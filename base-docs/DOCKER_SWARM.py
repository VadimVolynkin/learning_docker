# задачи swarm можно реализовать в ku8s


Позволяет собрать несколько докер-хостов в единый кластер.
Кластер будет распределять службы на отдельные хосты(обеспечивает доступность, балансировку нагрузки).

1 из хостов будет мастером, остальные - воркеры(node)

# инициализация менеджера swarm
# в выводе будет дана команда docker swarm join, которую нужно запустить на воркерах, чтобы они присоединились к менеджеру
docker swarm init 