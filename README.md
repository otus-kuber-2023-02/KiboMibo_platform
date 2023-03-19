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


# Выполнено ДЗ №2

 - [x] Основное ДЗ
 - [x] Задание с *
 - [x] Задание с **

## В процессе сделано:
 - собран образ paymentservice и запушен в dockerhub c тегами: kibomibo/otus-microservice-payment:v0.0.1 и kibomibo/otus-microservice-payment:v0.0.2
 - сделаны манифесты для paymentservice: replicaset, deployment
 - сделан манифест для аналога blue-green deployment
 - сделан манифест для reverse rolling update
 - сделаны манифесты для сервиса frontend: replicaset и depoyment
 - проведена проверка работоспособности healthProbe для сервиса frontend
 - сделан манифест для daemon-set node-exporter
 - решена проблема запуска подов daemon-set на мастер ноде

## Как запустить проект:
 - Запустить комманду kubectl apply -f frontend-deployment.yaml
 - Запустить комманду kubectl apply -f paymentservice-deployment.yaml

## Как проверить работоспособность:
 - Запустить комманду kubectl describe po $(kubectl get pods -l app=frontend -o=jsonpath='{.items[0].metadata.name}')
