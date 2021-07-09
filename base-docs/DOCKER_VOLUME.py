# https://docs.docker.com/engine/reference/commandline/volume_create/
# https://docs.docker.com/storage/volumes/

# =============================================================================================================================
# DOCKER VOLUME CLI
# =============================================================================================================================
docker volume create my_vol   # Создать новый том данных RW с драйвером local в /var/lib/docker/volumes/my_vol/_data
docker volume ls 	          # Список всех томов известных Docker
docker volume inspect my_vol  # Отображает информацию о томе
docker volume rm my_vol       # Удалить один или несколько томов
docker volume prune           # Удалить все неиспользуемые тома


# =============================================================================================================================
# VOLUME
# =============================================================================================================================
Тома не хранят данные в контейнере - соответственно не увеличивают размер контейнера.
Тома создаются докером здесь: /var/lib/docker/volumes/myapp_volume/_data
Тома не удаляются после удаления.
Для удаления анонимных томов есть --rm: docker run --rm -v /foo -v awesome:/bar busybox top
Тома предназначены для эффективного ввода-вывода.
Том может быть общим для нескольких контейнеров
Тома - предпочтительный способ хрнения данных в докере. Тома полностью управляются Docker.
В томах легче создавать резервные копии или переносить, чем в bind mount.
Драйверы томов позволяют хранить тома на удаленных узлах или у облачных провайдеров, шифровать содержимое томов или добавлять другие функции.
Команда docker service create используют только синтаксис --mount.
Тома могут использовать NFS(удаленное хранение инфы типа Amazon S3).
Тома полезны для резервного копирования, восстановления и миграции. Используйте флаг --volumes-from, чтобы создать новый контейнер, который монтирует этот том. 
Драйверы хранилища: Btrfs, ZFS, aufs, overlay и overlay2
--mount, -v, --volume   - это все разные варианты записи хранилищь

# примеры синтаксиса для томов
# ro - readonly, rw - read/write
docker run --mount source=myvol, target=/app, readonly
docker run --volume myvol:/app:rw
docker run -v myvol:/app:ro                        # -v name_vol_in_docker:/cotainer_path


# синтаксис --mount
type of the mount: bind, volume, tmpfs             # тип монтирования
source или src                                     # источник монтирования
destination, dst, or target                        # точка монтирования в контейнере
readonly                                           # только для чтения
volume-opt                                         # пара имя параметра и его значения



# пример в docker-compose.yml
version: "3.9"
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
      - myapp2:/home/node/app2
volumes:
  myapp:                                    # создаст новый том
  myapp2:
    external: true                          # будет подключен ранее созданный извне том. Если его нет - ошибка.


# =============================================================================================================================
# BIND MOUNT
# =============================================================================================================================. 
Файл или папка хоста по ее абсолютному пути монтируется в контейнер.
-v или --volume создаст папку, если папки или файла еще не существует.
--mount выдаст ошибку, если папки или файла еще не существует.
Докер рекомендует использовать синтаксис --mount.
Если локальная папка монтируется в непустую папку контейнера - ее содержимое будет скрыто содержимым локальной папки.
Контейнеру можно установить доступ только для чтения.

bind-propagation 
# указывает особенности расспространения монтирования.  
# обычно это не надо
# варианты: rprivate(по умолчанию), private, rshared, shared, rslave, slave


# пример --mount  синтаксиса
# source - папка хоста, target - папка контейнера
docker run -dit --name devtest --mount type=bind,source="$(pwd)"/target,target=/app nginx:latest


# пример -v синтаксиса(старый стиль)
# -v /local_path:/cotainer_path:ro 
docker run -dit --name devtest -v "$(pwd)"/target:/app nginx:latest



# =============================================================================================================================
# TMPFS
# =============================================================================================================================
Временное хранение данных в оперативной памяти. Доступно только в Linux.
После удаления контейнера данные в удаляются, каки точка монтирования.
Это полезно для временного хранения паролей, которые не нужно сохранять ни на хосте, ни в слое контейнера.
Нельзя использовать между несколькими контейнерами.
Докер рекомендует использовать синтаксис --mount.


# пример --mount синтаксиса
# tmpfs-size - размер монтируемого файла tmpfs в байтах. По умолчанию без ограничений.
# tmpfs-mode - файловый режим(о умолчанию 1777 - доступен для записи всем). 1770 - не доступен для чтения всем в контейнере. 
docker run -dit --name tmptest --mount type=tmpfs,destination=/app,tmpfs-mode=1770,tmpfs-size=10000 nginx:latest


# пример --tmpfs синтаксиса
docker run -dit --name tmptest --tmpfs /app nginx:latest











