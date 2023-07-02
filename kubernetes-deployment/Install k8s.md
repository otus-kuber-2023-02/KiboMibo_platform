Создал 4 виртуальные машины в YC:
	- 2 vCPU
	- 2Gb ram
	- 20Gb hdd
	
![[Screenshot 2023-07-02 at 19.16.45.png]]

На каждой машине отключен swap:
```bash
sudo swapoff -a
```

Проверил, что на машинах не совпадают MAC адреса и product_uuid:
	- master:  d0:0d:14:d7:b7:44 23000007-c6d4-d7b7-44d4-8d764e2dc76b
	- worker-01 d0:0d:70:23:0a:eb 23000007-c6c7-0230-aeb3-96e84fb61a21
	- worker-02 d0:0d:18:a9:31:65 23000007-c6d8-a931-6555-3726e9e6f647
	- worker-03 d0:0d:11:4f:cc:5e 23000007-c6d1-4fcc-5ea0-502b25071ed3

Проверил на доступность порт 6443 на всех нодах.

Установил containerd по [[ https://github.com/containerd/containerd/blob/main/docs/getting-started.md | инструкции ]] на все ноды.
Установил на ноды kubelet kubeadm kubectl

Первый запуск kubeadmin --init
```bash
sudo kubeadm init  --pod-network-cidr=192.168.0.0/24
[init] Using Kubernetes version: v1.27.3
[preflight] Running pre-flight checks
error execution phase preflight: [preflight] Some fatal errors occurred:
	[ERROR FileContent--proc-sys-net-bridge-bridge-nf-call-iptables]: /proc/sys/net/bridge/bridge-nf-call-iptables does not exist
	[ERROR FileContent--proc-sys-net-ipv4-ip_forward]: /proc/sys/net/ipv4/ip_forward contents are not set to 1
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`
```

Чтобы исправить ошибки:
```bash
#добавление модулей в загрузку
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

#Запустить модуль net filter
modprobe br_netfilter
#Запустить модуль overlay
modprobe overlay

#Включить поддержку bridge-nf-call-iptables и ip_forward
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# применить
sysctl --system

```
[[ https://github.com/containerd/containerd/issues/7388 | github issue]]
[[ https://github.com/containerd/containerd/issues/7388 | github issue ]]

Добавляем конфиг crictl
```yaml
#/etc/crictl.yaml
runtime-endpoint: "unix:///run/containerd/containerd.sock"
image-endpoint: "unix:///run/containerd/containerd.sock"
timeout: 10
debug: false
pull-image-on-create: false
disable-pull-on-run: false
```

Запускаем инициализацию control plane
```bash
kubeadm init --pod-network-cidr=192.168.0.0/24
```

Добавляем сетевые плагины:
```bash
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml -O
```
Раскоментируем переменную CALICO_IPV4POOL_CIDR установив значения 192.168.0.0/24 и применим

```bash
kubectl apply -f calico.yaml
```

Добавляем воркер ноды:
```bash
kubeadm join 10.128.0.27:6443 --token 6ypd63.8m4xrncy0691lazf \
	--discovery-token-ca-cert-hash sha256:ed78176ceecb4bf1637c2016c8a7d6a60dd5604adc1c928371787f81522667d0
```

```bash
$ kubectl get nodes
NAME             STATUS   ROLES           AGE   VERSION
kube-master      Ready    control-plane   67m   v1.27.3
kube-worker-01   Ready    <none>          51m   v1.27.3
kube-worker-02   Ready    <none>          42s   v1.27.3
kube-worker-03   Ready    <none>          34s   v1.27.3
```

Установка nginx deployment:
```
kibo@kube-master:~$ kubectl get po
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-5cf6fcbc8f-52z86   1/1     Running   0          2m4s
nginx-deployment-5cf6fcbc8f-gc84t   1/1     Running   0          2m4s
nginx-deployment-5cf6fcbc8f-nn8qz   1/1     Running   0          2m4s
nginx-deployment-5cf6fcbc8f-zdjsl   1/1     Running   0          2m4s
```