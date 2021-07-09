# =============================================================================================================================
# DOCKER COMPOSE CLI
# =============================================================================================================================
docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]


config             Validate and view the Compose file
build              Build or rebuild services
bundle             Generate a Docker bundle from the Compose file

scale              Set number of containers for a service
create             Create services
up                 Create and start containers
down               Stop and remove containers, networks, images, and volumes
pause              Pause services
unpause            Unpause services
start              Start services
stop               Stop services
restart            Restart services

events             Receive real time events from containers
logs               View output from containers
top                Display the running processes
port               Print the public port for a port binding

exec               Execute a command in a running container

ps                 List containers
images             List images

kill               Kill containers
rm                 Remove stopped containers
run                Run a one-off command

pull               Pull service images
push               Push service images

version            Show the Docker-Compose version information
help               Get help on a command


# ===== CLI OPTIONS =============================================================================================

-f, --file FILE             Specify an alternate compose file(default: docker-compose.yml)
-p, --project-name NAME     Specify an alternate project name(default: directory name)
--verbose                   Show more output
--log-level LEVEL           Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
--no-ansi                   Do not print ANSI control characters
-v, --version               Print version and exit
-H, --host HOST             Daemon socket to connect to

--tls                       Use TLS; implied by --tlsverify
--tlscacert CA_PATH         Trust certs signed only by this CA
--tlscert CLIENT_CERT_PATH  Path to TLS certificate file
--tlskey TLS_KEY_PATH       Path to TLS key file
--tlsverify                 Use TLS and verify the remote
--skip-hostname-check       Don't check the daemon's hostname against thename specified in the client certificate
--project-directory PATH    Specify an alternate working directory(default: the path of the Compose file)
--compatibility             If set, Compose will attempt to convert keys in v3 files to their non-Swarm equivalent
--env-file PATH             Specify an alternate environment file


# =============================================================================================================================
# MOST POPULAR DOCKER_COMPOSE COMMANDS AND FLAGS
# =============================================================================================================================

docker-compose up -d --build                                          #
docker-compose build                                                  #
docker-compose up                                                     #
docker-compose down                                                   # позволяет останавливать и удалять контейнеры

docker-compose ps                                                     # список контейнеров
docker-compose images                                                 # список образов
docker-compose logs -f [service name]                                 # журналы сервисов
docker-compose -f docker-compose.yml exec timescale psql -Upostgres   # выполнит вход в оболочку psql

docker-compose exec [service name] [command]                          # выполяет команду в работающем контейнере  


# =============================================================================================================================
# DOCKER-COMPOSE.YML version: "3.9"
# =============================================================================================================================

version: "3.9"
services:

  web:
    build: .                         # создаем сервис из dockerfile в этой папке
    ports:                           # внешний порт:порт контейнера
      - "5000:5000"
    volumes:                         # коннектим содержимое этой папки с папкой контейнера
      - .:/code
    environment:                     # переменные окружения
      - FLASK_ENV: development
      - DEBUG=1
    env_file:
    - ./Docker/api/api.env

  redis:
    image: "redis:alpine"            # создаем сервис из образа


# === environment
переменные окружения внутри docker-compose.yml
переменные окружения в environment приоритетнее переменных из env_file

# === env_file:                        
файл переменных окружения внутри docker-compose.yml 


# === файл .env в папке с docker-compose.yml             
по дефолту docker-compose.yml ищет переменные окружения в файле .env в этой же папке
переменную TAG=v1.5 в файле .env можно использовать в docker-compose.yml, например image: "webapp:${TAG}"
можно назначить другой файл с переменными используя --env-file в командной строке 
можно назначить другой файл с переменными используя env_file в docker-compose.yml  
значение TAG можно переопределить через shell: export TAG=v2.0
значение TAG можно переопределить docker-compose run -e TAG=v4.0 web python console.py

Приоритет поиска переменных окружения:
1.Compose file
2.Shell environment variables
3.Environment file .env
4.Dockerfile
5.Variable is not defined


# === --env-file 
запускает другой .env файл - .env.dev: docker-compose --env-file ./config/.env.dev up 