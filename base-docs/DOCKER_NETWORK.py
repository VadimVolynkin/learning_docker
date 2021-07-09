
Сервисы или контейнеры могут быть подключены к нескольким сетям одновременно. 
Сервисы или контейнеры могут взаимодействовать только через сети, к которым они подключены.

ip a (ip addr), ip link, ip -s (ip -stats)
ip tunnel
ip n (ip neighbor)
  
sudo ss -tlunp        # сетевые процессы
sudo netstat -tulpen

sudo ss -taunp        # все сетевые подключения
sudo netstat -atupen

sudo ss -tunp         # только установленные соединения

192.168.0.1           # адрес роутера в локальной сети
curl icanhazip.com    # внешний адрес

# tcp4/udp4 
0.0.0.0               # процесс прослушивает соединения с любого компьютера в сети
127.0.0.1             # процесс прослушивает только localhost и не может быть подключен к другим компьютерам в сети

# tcp6/udp6
::                    # процесс прослушивает соединения с любого компьютера в сети
::1                   # процесс прослушивает только localhost и не может быть подключен к другим компьютерам в сети

# характеристики сети в конфиге сети
"Name": "devdjango_default"
"Subnet": "192.168.16.0/20",
"Gateway": "192.168.16.1"

# характеристики контейнера в конфиге сети
"Name": "devdjango_nginx_1",
"EndpointID": "4b422bbe5eccd016c42d05be7dcd2a3c87fb9376e97f2279b58718009b7ad871",
"MacAddress": "02:42:c0:a8:10:04",
"IPv4Address": "192.168.16.4/20",
"IPv6Address": ""


# характеристики контейнера в конфиге контейнера
"Ports": {
      "80/tcp": [
        {
          "HostIp": "0.0.0.0",
          "HostPort": "80"
        },
        {
          "HostIp": "::",
          "HostPort": "80"
        }
      ]
    },

Для поддержки IPv6 нужно включить эту опцию в демоне Docker и перезагрузить его конфигурацию.
# =============================================================================================================================
# DOCKER NETWORK CLI
# =============================================================================================================================

docker network create my-net	                # Создать новую сеть
docker network connect my-net my-nginx	      # Подключить контейнер к сети
docker network disconnect my-net my-nginx   	# Отключить контейнер от сети
docker network rm my-net	                    # Удалить одну или несколько сетей
docker network ls 	                          # Список всех сетей известных демону Docker
docker network inspect my-net	                # Показать информацию о сети

# создание контейнера nginx и подключение его к сети my-net(сеть уже должна быть создана)
# публикация порта - порт_хоста:порт_контейнера
docker create --name my-nginx --network my-net --publish 8080:80 nginx:latest

# =============================================================================================================================
# BRIDGE
# =============================================================================================================================
Мостовые сети нужны для обмена данными между контейнерами на одном хосте Docker.
172.17.0.1
Сделать контейнер доступным извне можно пробросив порты.

# ===== СЕТЬ bridge по умолчанию
Контейнеры, для которых не указан параметр --network автоматически подключается к сети bridge (сеть с драйвером моста по умолчанию). В сети моста по умолчанию контейнеры обмениваются данными только по IP.
Чтобы удалить контейнер из сети моста по умолчанию, необходимо остановить контейнер и воссоздать его с другими параметрами сети.

# Включить пересылку из контейнеров Docker во внешний мир
По умолчанию трафик из контейнеров, подключенных к сети моста по умолчанию, не пересылается во внешний мир. Чтобы включить пересылку, нужно изменить две настройки. Это не команды Docker, и они влияют на ядро хоста Docker.

sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT

# Настройка параметров сети bridge по умолчанию
Параметры для сети bridge по умолчанию находятся в файле daemon.json. После изменений необходимо перезапустить докер.

{
  "bip": "192.168.1.5/24",
  "fixed-cidr": "192.168.1.5/25",
  "fixed-cidr-v6": "2001:db8::/64",
  "mtu": 1500,
  "default-gateway": "10.20.1.1",
  "default-gateway-v6": "2001:db8:abcd::89",
  "dns": ["10.20.1.2","10.20.1.3"]
}

# ===== СОБСТВЕННЫЕ СЕТИ С ДРАЙВЕРОМ МОСТА
В пользовательской сети моста контейнеры могут разрешать друг друга по DNS.


# =============================================================================================================================
# OVERLAY
# =============================================================================================================================
Нужны для связи между контейнерами на разных демонах Docker. Эта стратегия устраняет необходимость маршрутизации на уровне ОС между этими контейнерами. 
Оверлейные сети соединяют вместе несколько демонов Docker и позволяют службам роя взаимодействовать друг с другом. 
Подходят для связи между службой роя и контейнером.



# Как работает сеть с драйвером overlay
Драйвер оверлейной сети создает распределенную сеть между несколькими хостами демонов Docker. 
Эта сеть находится поверх (накладывается) на сети, зависящие от хоста, позволяя подключенным к ней контейнерам (включая контейнеры служб роя) безопасно обмениваться данными при включенном шифровании. 
Docker прозрачно обрабатывает маршрутизацию каждого пакета к и от правильного хоста демона Docker и правильного контейнера назначения.


В момент инициализации рой или присоединения хоста Docker к существующему рою, на этом хосте Docker создаются 2 новые сети:

1. оверлейная сеть ingress(входящая)
Обрабатывает трафик управления и данных, связанный с услугами роя. Когда вы создаете службу роя и не подключаете ее к определяемой пользователем оверлейной сети, она по умолчанию подключается к входящей сети.

2. сеть моста docker_gwbridge
Соединяет отдельный демон Docker с другими демонами, участвующими в рое.


# КАК СОЗДАТЬ СОБСТВЕННУЮ ОВЕРЛЕЙНУЮ СЕТЬ

# 1. Настройки брандмауера
В брандмауэре должны быть открыты порты к каждому хосту Docker в оверлейной сети:
- TCP-порт 2377 для обмена данными по управлению кластером
- TCP и UDP порт 7946 для связи между узлами
- UDP-порт 4789 для оверлейного сетевого трафика

# 2. Инициализация докер демона
Можно инициализировать демона докера в качестве менеджера роя командой docker swarm init
или присоединить его к существующему рою, используя соединение роя докеров.
Это создает входящую оверлейную сеть по умолчанию, которая по умолчанию используется службами роя. Это нужно делать, даже если не планируете использовать Swarm. 
После этого можно создавать дополнительные определяемые пользователем оверлейные сети. 

# 3. Создание оверлейной сети
Конфигурации оверлейных сетей для роя и оверлейных сетей для автономных контейнеров различны.
Можно указать диапазон IP-адресов, подсеть, шлюз и другие параметры.

# создание сети для swarm
# трафик управления службами swarm по умолчанию зашифрован алгоритмом AES в режиме GCM, меняет шифр каждые 12 часов
# дополнительно можно зашифровать трафик приложений: --opt encrypted - включит шифрование IPSEC на уровне vxlan
# -p published=8080,target=80,protocol=udp  Присоединяет 8080 порт сети маршрутизатора к порту 80 swarm-сервиса
docker network create -d overlay my-overlay -p published=8080,target=80,protocol=udp

# создание сети для swarm и автономных контейнеров на других демонах
# --attachable позволяет подключать автономные контейнеры
# -p 8080:80 порт_оверлей_сети:порт_контейнера
docker network create -d overlay --attachable my-attachable-overlay -p 8080:80


Посмотреть задачи сервиса можно так: tasks.<DNS service-name>.

# =============================================================================================================================
# HOST
# =============================================================================================================================
Сетевой стек этого контейнера не изолирован от хоста Docker (контейнер разделяет сетевое пространство имен хоста).
Контейнер не получает свой собственный IP-адрес. При запуске контейнера на порту 80, он будет доступен на IP_адресе-хоста:80. 
Host работает только на хостах Linux.
Хост-сеть можно использовать для службы роя, передав --network host команде создания службы docker. Управляющий трафик по прежнему будет идти через оверлейную сеть, но трафик контейнеров будет идти через хост машину напрямую.

# Где использовать
Лучше всего подходят, когда сетевой стек контейнера не должен быть изолирован от хоста Docker, но другие аспекты контейнера должны быть изолированы.

# =============================================================================================================================
# IPvlan
# =============================================================================================================================

Драйвер IPvlan дает пользователям полный контроль над адресацией IPv4 и IPv6.
Драйвер VLAN дополняет его, предоставляя операторам полный контроль над маркировкой VLAN уровня 2 и даже маршрутизацией IPvlan L3 для пользователей, заинтересованных в базовой сетевой интеграции. Это нужно для развертываний наложения, которые абстрагируются от физических ограничений.


IPvlan L2 mode

IPvlan 802.1q trunk L2 mode

VLAN ID 20

VLAN ID 30

IPvlan L3 mode

Dual stack IPv4 IPv6 IPvlan L2 mode

Dual stack IPv4 IPv6 IPvlan L3 mode

VLAN ID 40






# =============================================================================================================================
# Macvlan
# =============================================================================================================================
Назначает MAC-адрес контейнеру, чтобы он отображался как физическое устройство, подключенное к физической сети. Такая портебность часто возникает в старых приложениях, ожидающих физического подключения.
Демон Docker направляет трафик в контейнеры по их MAC-адресам. 


# КАК СОЗДАТЬ СЕТЬ Macvlan
Необходимо назначить физический интерфейс на хосте Docker(будет использоваться для macvlan), подсеть и шлюз для macvlan. 
Можно такжн изолировать сети macvlan, используя различные физические сетевые интерфейсы.
Сетевое оборудование должно поддерживать «беспорядочный режим», когда одному физическому интерфейсу может быть назначено несколько MAC-адресов.

Сеть macvlan может быть вв 2 режимах:

# bridge mode
трафик macvlan проходит через физическое устройство на хосте.
--aux-addresses запрещает использование IP адреса в сети.

docker network create -d macvlan \
  --subnet=192.168.32.0/24 \
  --ip-range=192.168.32.128/25 \
  --gateway=192.168.32.254 \
  --aux-address="my-router=192.168.32.129" \
  -o parent=eth0 macnet32

# trunk bridge mode 802.1q
трафик проходит через субинтерфейс 802.1q, который Docker создает на лету. Это позволяет контролировать маршрутизацию и фильтрацию на более детальном уровне. 

docker network create -d macvlan \
  --subnet=192.168.50.0/24 \
  --gateway=192.168.50.1 \
  -o parent=eth0.50 macvlan50