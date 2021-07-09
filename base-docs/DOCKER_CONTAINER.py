
сослаться на контейнер в команде можно либо используя его ID, либо имя

# =============================================================================================================================
# MOST POPULAR CONTAINER COMMANDS AND FLAGS
# =============================================================================================================================
docker create --name some my_img                      # Создает новый контейнер с именем some
docker rename old new                                 # Переименовать контейнер

docker run -it my_image bash                          # запускает bash в интерактивном режиме
docker run -d my_image                                # создает и запускает контейнер в фоновом режиме
docker run -it my_image my_command                    # создает и запускает контейнер, выполняет в терминале команду
docker run -i -t -p 1000:8000 --rm my_image           # создает и запускает контейнер на порту 1000, удаляет по завершению

docker container ls -a -s                             # показывает размер всех контейнеров

docker inspect my_container                           # выводит подробные сведения о контейнере
docker logs my_container                              # выводит логи контейнера

docker stop my_container                              # корректно останавливает работающий контейнер
docker kill my_container                              # грубо останавливает работающий контейнер
docker kill $(docker ps -q)                           # грубо останавливает все работающие контейнеры
docker rm $(docker ps -a -q)                          # удаляет все остановленные контейнеры


-i, --interactive 
# поток STDIN поддерживается в открытом состоянии даже если контейнер к STDIN не подключён
# позволяет вводить информацию из терминала в контейнер

-t, --tty         
# псевдотерминал, который соединяет используемый терминал с потоками STDIN и STDOUT контейнера
# позволяет получать информацию из контейнера
# чтобы взаимодействовать с контейнером через терминал нужно совместно использовать флаги -i и -t

-it
# комбинация -i и -t создает сессию терминала в контейнере, с ним можно взаимодействовать через терминал вызова
# для выхода из сессии, введите в терминал exit
# для рвботы с Alpine нужно использовать sh(bash в нем не установлен)

-p, --port
# интерфейс для взаимодействия контейнера с внешним миром. 
# Конструкция 1000:8000 перенаправляет порт Docker 8000 на порт 1000 компьютера, на котором выполняется контейнер. 

--rm 
# автоматически удаляет контейнер после того, как его выполнение завершится.

-d, --detach
# запускает контейнер в фоновом режиме. Это позволяет использовать терминал, из которого запущен контейнер, для выполнения других команд во время работы контейнера.

-a, --all
# выводит сведения обо всех контейнерах, а не только о выполняющихся

-q, --quiet 
# показывать только ID контенеров

-s, --size
# выводит размеры контейнеров


# =============================================================================================================================
# DOCKER CONTAINER CLI
# =============================================================================================================================
docker run [OPTIONS] IMAGE [COMMAND] [ARG...] # Выполняет команду в новом контейнере
docker create                 # Создает новый контейнер
docker rename                 # Переименовать контейнер
docker start                  # Запускает один или несколько остановленных контейнеров
docker stop                   # Останавливает один или несколько запущенных контейнеров
docker restart                # Перезапускает один или несколько запущенных контейнеров
docker kill                   # Грубое завершение запущенного контейнера
docker rm                     # Удаляет один или несколько контейнеров
docker container prune        # Удалить все остановленные контейнеры

diff         # Проверяет изменения в файловой системе контейнера
commit       # Создать новый образ из измененного контейнера
update       # Обновляет конфигурацию одного или нескольких контейнеров
cp           # Копирует файлы/каталоги из контейнера в HOSTDIR или STDOUT
export       # Экспортирует файловую систему контейнера в tar архив

exec         # Выполняет команду в запущенном контейнере

docker ps 	            # Список работающих контейнеров
docker container ls     # Список работающих контейнеров
stats        # Выводит в реальном времени информацию о потребляемых контейнером ресурсах
inspect      # Выводит детальную информацию об одном или нескольких контейнерах
logs         # Отображает логи контейнера
attach       # Подключиться к запущенному контейнеру: standard input, output, and error streams
port         # Отображение общего списка портов для конкретного контейнера
events 	     # Получает события сервера в режиме реального времени

top          # Отображает запущенные в контейнере процессы
pause        # Ставит на паузу все процессы контейнера
unpause      # Снимает с паузы все процессы контейнера

wait         # Блокирует контейнер до его остановки, а затем выводит код завершения


# =============================================================================================================================
# FLAGS
# =============================================================================================================================

--add-host 		         # Add a custom host-to-IP mapping (host:ip)
--attach , -a 		     # Attach to STDIN, STDOUT or STDERR
--blkio-weight 		     # Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)
--blkio-weight-device 	 # Block IO weight (relative device weight)
--cap-add 		         # Add Linux capabilities
--cap-drop 		         # Drop Linux capabilities
--cgroup-parent 		 # Optional parent cgroup for the container
--cgroupns 		         # API 1.41+ Cgroup namespace to use (host|private) 'host': Run the container in the Docker host's cgroup namespace 'private': Run the container in its own private cgroup namespace '': Use the cgroup namespace as configured by the default-cgroupns-mode option on the daemon (default)
--cidfile 		         # Write the container ID to the file
--cpu-count 		     # CPU count (Windows only)
--cpu-percent 		     # CPU percent (Windows only)
--cpu-period 		     # Limit CPU CFS (Completely Fair Scheduler) period
--cpu-quota 		     # Limit CPU CFS (Completely Fair Scheduler) quota
--cpu-rt-period 		 # API 1.25+ Limit CPU real-time period in microseconds
--cpu-rt-runtime 		 # API 1.25+ Limit CPU real-time runtime in microseconds
--cpu-shares , -c 		 # CPU shares (relative weight)
--cpus 		             # API 1.25+ Number of CPUs
--cpuset-cpus 		     # CPUs in which to allow execution (0-3, 0,1)
--cpuset-mems 		     # MEMs in which to allow execution (0-3, 0,1)
--detach , -d 		     # Run container in background and print container ID
--detach-keys 		     # Override the key sequence for detaching a container
--device 		         # Add a host device to the container
--device-cgroup-rule     # Add a rule to the cgroup allowed devices list
--device-read-bps 		 # Limit read rate (bytes per second) from a device
--device-read-iops 		 # Limit read rate (IO per second) from a device
--device-write-bps 		 # Limit write rate (bytes per second) to a device
--device-write-iops      # Limit write rate (IO per second) to a device
--disable-content-trust true # Skip image verification
--dns 		             # Set custom DNS servers
--dns-opt 		         # Set DNS options
--dns-option 		     # Set DNS options
--dns-search 		     # Set custom DNS search domains
--domainname 		     # Container NIS domain name
--entrypoint 		     # Overwrite the default ENTRYPOINT of the image
--env , -e 		         # Set environment variables
--env-file 		         # Read in a file of environment variables
--expose 		         # Expose a port or a range of ports
--gpus 		             # API 1.40+ GPU devices to add to the container ('all' to pass all GPUs)
--group-add 		     # Add additional groups to join
--health-cmd 		     # Command to run to check health
--health-interval 		 # Time between running the check (ms|s|m|h) (default 0s)
--health-retries 		 # Consecutive failures needed to report unhealthy
--health-start-period    # API 1.29+ Start period for the container to initialize before starting health-retries countdown (ms|s|m|h) (default 0s)
--health-timeout 		 # Maximum time to allow one check to run (ms|s|m|h) (default 0s)
--help 		             # Print usage
--hostname , -h 		 # Container host name
--init 		             # API 1.25+ Run an init inside the container that forwards signals and reaps processes
--interactive , -i 		 # Keep STDIN open even if not attached
--io-maxbandwidth 		 # Maximum IO bandwidth limit for the system drive (Windows only)
--io-maxiops 		     # Maximum IOps limit for the system drive (Windows only)
--ip 		             # IPv4 address (e.g., 172.30.100.104)
--ip6 		             # IPv6 address (e.g., 2001:db8::33)
--ipc 		             # IPC mode to use
--isolation 		     # Container isolation technology
--kernel-memory 		 # Kernel memory limit
--label , -l 		     # Set meta data on a container
--label-file 		     # Read in a line delimited file of labels
--link 		             # Add link to another container
--link-local-ip 		 # Container IPv4/IPv6 link-local addresses
--log-driver 		     # Logging driver for the container
--log-opt 		         # Log driver options
--mac-address 		     # Container MAC address (e.g., 92:d0:c6:0a:29:33)
--memory , -m 		     # Memory limit
--memory-reservation     # Memory soft limit
--memory-swap 		     # Swap limit equal to memory plus swap: '-1' to enable unlimited swap
--memory-swappiness -1 	 # Tune container memory swappiness (0 to 100)
--mount 		         # Attach a filesystem mount to the container
--name 		             # Assign a name to the container
--net 		             # Connect a container to a network
--net-alias 		     # Add network-scoped alias for the container
--network 		         # Connect a container to a network
--network-alias 		 # Add network-scoped alias for the container
--no-healthcheck 		 # Disable any container-specified HEALTHCHECK
--oom-kill-disable 		 # Disable OOM Killer
--oom-score-adj 		 # Tune host's OOM preferences (-1000 to 1000)
--pid 		             # PID namespace to use
--pids-limit 		     # Tune container pids limit (set -1 for unlimited)
--platform 		         # API 1.32+ Set platform if server is multi-platform capable
--privileged 		     # Give extended privileges to this container
--publish , -p 		     # Publish a container's port(s) to the host
--publish-all , -P 		 # Publish all exposed ports to random ports
--pull 	missing 	     # Pull image before running ("always"|"missing"|"never")
--read-only 		     # Mount the container's root filesystem as read only
--restart 	no 	         # Restart policy to apply when a container exits
--rm 		             # Automatically remove the container when it exits
--runtime 		         # Runtime to use for this container
--security-opt 		     # Security Options
--shm-size 		         # Size of /dev/shm
--sig-proxy true 	     # Proxy received signals to the process
--stop-signal 	SIGTERM  # Signal to stop a container
--stop-timeout 		     # API 1.25+ Timeout (in seconds) to stop a container
--storage-opt 		     # Storage driver options for the container
--sysctl 		         # Sysctl options
--tmpfs 		         # Mount a tmpfs directory
--tty , -t 		         # Allocate a pseudo-TTY
--ulimit 		         # Ulimit options
--user , -u 		     # Username or UID (format: <name|uid>[:<group|gid>])
--userns 		         # User namespace to use
--uts 		             # UTS namespace to use
--volume , -v 		     # Bind mount a volume
--volume-driver 		 # Optional volume driver for the container
--volumes-from 		     # Mount volumes from the specified container(s)
--workdir , -w 		     # Working directory inside the container




# =============================================================================================================================
# ПРИМЕРЫ
# =============================================================================================================================

docker run -it nginx bash                            # create container and run command bash
docker run -p 8080:80 nginx                 
docker run -p 8080:80 -d nginx -d --not interactive































