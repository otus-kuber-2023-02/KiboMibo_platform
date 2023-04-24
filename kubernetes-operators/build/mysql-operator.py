import kopf
from kubernetes.client import ApiException
import yaml
import kubernetes
import time
from jinja2 import Environment, FileSystemLoader


def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.safe_load(stream=yaml_manifest)
    return json_manifest


def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while (not job_finished) and any(job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            if job.metadata.name == jobname:
                print(f"job with { jobname }  found,wait untill end")
                if job.status.succeeded == 1:
                    print(f"job with { jobname }  success")
                    job_finished = True

def delete_success_jobs(mysql_instance_name):
    print("start deletion")
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
        jobname = job.metadata.name
        if (jobname == f"backup-{mysql_instance_name}-job") or (jobname == f"restore-{mysql_instance_name}-job"):
            if job.status.succeeded == 1:
                api.delete_namespaced_job(jobname, 'default', propagation_policy='Background')

# Функция, которая будет запускаться при создании объектов тип MySQL:
@kopf.on.create('otus.homework', 'v1', 'mysqls')
def mysql_on_create(body, spec, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image'] # cохраняем в переменные содержимое описания MySQL из CR
    password = body['spec']['password']
    database = body['spec']['database']
    storage_size = body['spec']['storage_size']
    
    # Генерируем JSON манифесты для деплоя
    # persistent_volume = render_template('mysql-pv.yml.j2', {'name': name, 'storage_size': storage_size})
    service = render_template('mysql-service.yml.j2', {'name': name})

    deployment = render_template('mysql-deployment.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database
    })

    restore_job = render_template('restore-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})

    # Определяем, что созданные ресурсы являются дочерними к управляемому CustomResource:
    # kopf.append_owner_reference(persistent_volume, owner=body)
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)

    coreAPI = kubernetes.client.CoreV1Api()
    
    try:
        # Создаем mysql PVC:
        persistent_volume_claim = render_template('mysql-pvc.yml.j2', {'name': name, 'storage_size': storage_size})
        coreAPI.create_namespaced_persistent_volume_claim('default', persistent_volume_claim)
        kopf.append_owner_reference(persistent_volume_claim, owner=body) # addopt

        # Создаем backup PVC:
        backup_pvc = render_template('backup-pvc.yml.j2', {'name': name, 'storage_size': storage_size})
        coreAPI.create_namespaced_persistent_volume_claim('default', backup_pvc)
        print("backup pvc is created")
    except kubernetes.client.ApiException as e:
        print("create backup pvc: %s" % e)

    # Создаем mysql SVC:
    coreAPI.create_namespaced_service('default', service)

    # Создаем mysql Deployment:
    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment('default', deployment)

    # Пытаемся восстановиться из backup
    try:
        batchAPI = kubernetes.client.BatchV1Api()
        batchAPI.create_namespaced_job('default', restore_job)
    except kubernetes.client.ApiException:
        pass
    

@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body: dict, **kwargs: dict):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']

    delete_success_jobs(name)

    # Cоздаем backup job:
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    try:
        api.create_namespaced_job('default', backup_job)
        wait_until_job_end(f"backup-{name}-job")
    except kubernetes.client.ApiException:
        pass

    return {'message': "mysql and its children resources deleted"}
