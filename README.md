# KiboMibo_platform
KiboMibo Platform repository


# Выполнено ДЗ №1

 - [x] Основное ДЗ
 - [x] Задание со *

## В процессе сделано:
 - Создан Dockerfile для web сервера
 - Написан манифест web-pod.yaml для развертывания в среде k8s с дополнительным контейнером инициализации
 - Для дополнительного задания проверен запуск приложения microservice-demo-frontend, для корректного запуска приложения необходимо для контейнера добавить env переменные.

## Как запустить проект:
 - Запустить комманду kubectl apply -f web-pod.yaml
 - Запустить комманду kubectl apply -f frontend-pod-healthy.yaml


## Как проверить работоспособность:
 - Перейти по ссылке http://localhost:8000/index.html
 - Выполнить комманду kubectl get po frontend
