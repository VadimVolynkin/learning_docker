# =============================================================================================================================
# DOCKERFILE
# инструкция для создания Docker Image из которого затем будет создан контейнер
# =============================================================================================================================
https://docs.docker.com/engine/reference/builder/

# содержит инструкции для сборки контейнера и определение его поведения при старте
# должен начинаться с инструкции FROM, или с инструкции ARG, за которой идёт FROM
# поверх базового образа можно добавлять дополнительные слои

# все слои image - только для чтения
# контейнер создает над слоями image "тонкий слой" - для записи

# =============================================================================================================================
# РЕКОМЕНДАЦИИ ПО СОЗДАНИЮ DOCKERFILE
# =============================================================================================================================
Используйте официальные образы.
Не устанавливайте в образы пакеты, без которых можно обойтись.
Размещайте команды, вероятность изменения которых высока, ближе к концу файла.
Используйте Alpine Linux там, где это возможно - он мало весит. Для питона лучше другая сборка типа buster.
Пользуйтесь файлом .dockerignore.
Объединяйте инструкции по установки пакетов в 1:

RUN apt-get update && apt-get install -y \
    package-one \
    package-two \
    package-three
 && rm -rf /var/lib/apt/lists/*

Создать образ с имене и тегом можно так:
docker build -t image: tag .
docker build -t image: tag -f dockerfile.dev .
docker build -t image: tag --no-cache=true .
# если dockerfile находися в текущей папке, то она является контекстом по умолчанию.
# если запускать dockerfile расположенный в другом месте, то контекстом является папка в которой вызывается docker build -f


RUN . /opt/venv/bin/activate && pip install -r requirements.txt
# активировать вирт окружение и запускать команды в нем нужно в 1 операции RUN, тк разные операции - разные процессы

# =============================================================================================================================
# ИНСТРУКЦИИ DOCKERFILE
# =============================================================================================================================

FROM python:3.7.2-alpine3.8 AS base
FROM scratch
# задаёт базовый (родительский) образ. Рекомендуется всегда прописывать конкретную версию.
# FROM scratch - без базового образа, с ноля
# Образ может быть ссылкой на гит
# AS - имя шага, используется при многоступенчатой сборке

# в примере выбран образ на основе Alpine Linux + python 3.7.2 + зависимости для корректной работы python 3.7.2
# вес чистой alpine - около 5мб, вес alpine с зависимостями - около 29мб, конечный образ с питоном - около 78мб
# уменьшать размер образов можно с помощью технологии многоступенчатой сборки


COPY . ./app
COPY Pipfile* /backend/
COPY --chown=myuser:mygroup src dest
COPY --chown=1000:1000 files* /somedir/
COPY --from=<stage_name>
# копирует файлы и папки текущей директории в контейнер в папку ./app
# если целевая папка ./app не существует, то будет создана.
# можно копировать файлы сразу с заменой прав
# можно копировать артефакты из стейджа при мультистейджинге FROM .. AS <stage_name>
# как и ADD сравнивает контрольные суммы копируемых файлов с кешем. Если не совпали - будут пересобраны все следующие слои.

ADD . .
ADD Pipfile* /backend/
ADD https://raw.githubusercontent.com/discdiver/pachy-vid/master/sample_vids/vid1.mp4 my_app_directory
ADD --chown=myuser:mygroup src dest
ADD --chown=1000:1000 files* /somedir/
ADD [--chown=<user>:<group>] ["src", "dest"]
# делает тоже что и COPY + другие возможности
# может добавлять в контейнер файлы, загруженные из удалённых источников(можно задать ссылку)
# может распаковывать локальные .tar-файлы
# в примере ADD копирует данные из интернета в папку контейнера /my_app_directory.
# можно копировать файлы сразу с заменой прав
# относительный путь в контейнере  строится относительно WORKDIR
# как и COPY сравнивает контрольные суммы копируемых файлов с кешем. Если не совпали - будут пересобраны все следующие слои.

RUN apk update && apk upgrade && apk add bash
RUN python app.py
RUN ["python", "app.py"]     
# выполняет команду и создаёт слой образа
# часто используется для установки в образы дополнительных пакетов
# новые пакеты часто устанавливаются через пакетные менеджеры со списком пакетов: RUN pip install requirements.txt
# Объединение команд в 1 инструкцию RUN(как в примере) позволяет записать все в 1 слой. Так читабельней.
# apk — Alpine Linux package manager(менеджер пакетов Alpine Linux). В другой базовой ОС, например Ubuntu, будет менеджер apt-get
# команда может быть использована в shell-форме или exec-форме 


CMD ["executable","param1","param2"] (exec form, this is the preferred form)
CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
CMD command param1 param2 (shell form)
# Команда с аргументами, которую нужно выполнить после запуска контейнера. Аргументы могут быть переопределены при запуске. Аргументы командной строки, передаваемые docker run, переопределяют аргументы CMD в Dockerfile.
# В файле может присутствовать лишь одна инструкция CMD. Если их несколько - сработает последняя.
# команда может быть использована в exec-форме или shell-форме
# Если в эту инструкцию не входит упоминание исполняемого файла, тогда в файле должна присутствовать инструкция ENTRYPOINT. В таком случае обе эти инструкции должны быть представлены в формате JSON.


ENTRYPOINT ["executable", "param1", "param2"]
ENTRYPOINT command param1 param2
# Команда с аргументами для вызова во время выполнения контейнера. Аргументы не переопределяются параметрами командной строки. Вместо этого аргументы командной строки добавляются к аргументам из ENTRYPOINT. 
# команда может быть использована в exec-форме(рекомендовано) или shell-форме.
# можно переопределить используя docker run --entrypoint


LABEL multi.label1="value1" multi.label2="value2" other="value3"
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
# описывает метаданные. Например — кто создал и поддерживает образ.
# смореть LABEL можно так: docker image inspect command --format


ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
ENV MY_NAME="John Doe" MY_CAT=fluffy
# устанавливает постоянные переменные среды, доступные в контейнере во время его выполнения
# хорошо подходит для задания констант, используемых в Dockerfile в нескольких местах - так их проще менять.
# можно переопредедить при запуске так: docker run --env <key>=<value>
# переменные ENV всегда переопределяют одноименные переменные ARG

ARG my_var=my_default_value
# задаёт переменную со значением по умолчанию для использования во время сборки.
# В отличие от ENV-переменных, ARG-переменные недоступны в контейнере, они не сохраняются после сборки,
# но они влияют на валидность кеша в момент первого использования этой ARG.
# значение для ARG можно передать из командной строки: docker build --build-arg var=value
# ARG-переменные можно использовать для задания из командной строки в процессе сборки образа значений ENV-переменных
# докер имеет предопределенные ARG:
# HTTP_PROXY
# http_proxy
# HTTPS_PROXY
# https_proxy
# FTP_PROXY
# ftp_proxy
# NO_PROXY
# no_proxy


WORKDIR /path/to/workdir
# задаёт абсолютный путь к рабочей директории для выполнения последующих инструкций: COPY, ADD, RUN, CMD и ENTRYPOINT
# автоматически создаёт директорию, если она не существует
# можно задать относительный путь, можно использовать несколько WORKDIR в 1 dockerfile

EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 80(по умолчанию TCP)
EXPOSE 80 443
# указывает какой порт открыть для связи с контейнером, и с каким протроколом. Можно оба протоколо.
# сама инструкция порты не открывает - это документация к работе с портами контейнера. 
# открыть все порты из EXPOSE можно так: docker run image_name -P
# открыть порт или настроить перенаправление можно так: docker run image_name -p 5432:5432
# для связи между контейнерами также можно использовать docker network

VOLUME ["/var/log/"]
VOLUME /var/log/
VOLUME /var/log /var/db
# создаёт точку монтирования для работы с постоянным хранилищем


USER user:group
USER UID:GID
# указывает кто будет запускать последующие команды
# при указании группы пользователь будет иметь членсво только в этой группе, другие будет проигнорированы
# если у пользователя нет группы - он получает группу root


STOPSIGNAL signal
# устанавливает сигнал для выхода из контейнера


ONBUILD ADD . /app/src
# Определяет инструкции, которые будут выполнены на следующем этапе сборки нового образа на основании этого образа. Обычно используется в образах, которые являются базой для создания дочерних образов. 
# Инструкции ONBUILD будут выполнены до следующего FROM.
# работает только вместе с инструкциями перечисленными выше в этом списке

SHELL ["powershell", "-command"]
# определяет какой shell используется по дефолту: cmd /S /C или powershell

HEALTHCHECK [OPTIONS] CMD command
# проверяет работоспособность контейнера путем запуска указанной команды в нем



# =============================================================================================================================
# КЕШИРОВАНИЕ
# ускоряет сборку образов
# =============================================================================================================================
Docker ищет в своем кеше образы, представляющие то, что получается на промежуточных этапах сборки других образов. 
Если есть - берет их вместо создания заново.
Если кэш недействителен, то инструкция, в ходе выполнения которой это произошло, выполняется, создавая новый слой без использования кэша. Все инструкции последующие инструкции создаются заново в обязательном порядке. Помещайте инструкции, вероятность изменения которых высока ближе к концу Dockerfile.

ВАЖНО: Если в Dockerfile есть инструкция RUN pip install -r requirements.txt, то содержимое requirements.txt не сравнивается. Это создает проблему в случае изменения пакетов. Решение в копировании через COPY:

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/

Инструкции ADD и COPY требуют проверки содержимого файла или файлов при формировании образа, чтобы решить можно ли воспользоваться кэшем. Контрольная сумма файлов в этих инструкциях сравнивается с контрольной суммой файлов промежуточных образов в кэше. Если не равно - кэш недействителен и образ создается заново.

При создании образа кэширование можно вообще отключить: docker build --no-cache. 


# =============================================================================================================================
# МНОГОСТУПЕНЧАТАЯ СБОРКА ОБРАЗОВ
# =============================================================================================================================
Такая сборка содержит несколько инструкций FROM.
Это позволяет настроить выборочное копирование файлов из одной ступени сборки в следующую. Такие файлы называют артефактами сборки. Так можно избавиться от ненужного - уменьшить размер.
Многоступенчатая сборка приводит к усложнению поддержки образов. Обычно без нее можно обойтись.

Вот как работает каждая инструкция FROM:
    Она начинает новый шаг сборки.
    Она не зависит от того, что было создано на предыдущем шаге сборки.
    Она может использовать базовый образ, отличающийся от того, который применялся на предыдущем шаге.


FROM alpine:latest as stage_name 
# так можно задать имя для stage

COPY --from=stage_name /path/to/files .
COPY --from=0   
# так можно достать файлы из образа                        #  
# --from может быть:
# - числом (порядковый номер stage в этом dokerfile, 0 - первый)
# - именем stage заданным через FROM as
# - любым образом доступным FROM

# =============================================================================================================================
# ФАЙЛ .dockerignore
# =============================================================================================================================
Содержит список файлов и папок, в виде имён или шаблонов, которые Docker должен игнорировать в ходе сборки образа.
Файл должен находиться в той же директории что и dockerfile.

# +++
Позволяет исключать из состава образа файлы, содержащие секретные сведения наподобие логинов и паролей.
Позволяет уменьшить размер образа, избавляясь от ненужного.
Даёт возможность уменьшить число поводов для признания недействительным кэша при сборке похожих образов(если изменится ненужный файл, например лог). Пример:

*.jpg    # проигнорирует все файлы с расширением jpg 
videos   # проигнорирует папку videos и все ее содержимое


# ===== КАК УЗНАТЬ РАЗМЕР КОНТЕЙННЕРОВ И ОБРАЗОВ
docker container ls -s                 # примерный размер выполняющегося контейнера
docker image ls                        # размеры образов
docker image history my_image:my_tag   # размеры промежуточных образов, из которых собран образ
docker image inspect my_image:tag      # подробные сведения об образе, в том числе — размер каждого его слоя(почти тоже что и промеж. образ).











