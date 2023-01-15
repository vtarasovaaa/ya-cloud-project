# ya-cloud-project

Итоговое задание по курсу "Инженер облачных сервисов"

- статичный фронт, реализован с помощью object storage
- бэк реализован с помощью Serverless Containers
- используется YDB


## Скрипты для автоматизации 

### Подготовительный этап

1. Убедиться, что установлена и настроена [Yandex CLI](https://cloud.yandex.ru/docs/cli/quickstart)

2. Проставить все енвы


    yc iam access-key create --service-account-name ya-cloud-project-notes

Сохранить key_id и secret, потом заново эти значения получить нельзя

    export KEY_ID=...  // сюда key_id
    export SECRET_KEY=...  // сюда secret

Узнать имя базы можно так
    
    yc ydb database get --name notes | grep endpoint
    export YDB_ENDPOINT=grpcs://ydb.serverless.yandexcloud.net:2135
    export YDB_DATABASE=...  // сюда то, что написано после /?database= из вывода первой команды

Оставшиеся енвы

    export SERVICE_ACCOUNT_ID=$(yc iam service-account get --name ya-cloud-project-notes | grep id | grep -v folder | cut -c5-)
    export FOLDER_ID=$(yc config get folder-id)
    export OAUTH_TOKEN=$(yc config get token)
    export CLOUD_ID=$(yc config get cloud-id)


### Обновление версии фронта 

Для начала надо установить и настроить [s3cmd](https://cloud.yandex.ru/docs/storage/tools/s3cmd#setup), 
используя ключи для сервисного аккаунта, сгенерированные выше

Затем можно обновлять

    . scripts/deploy-front.sh

### Обновление версии бэка

    . scripts/deploy-back.sh v1.1.6

здесь `v1.1.6` - номер новой версии


### Изменение количества реплик

В скрипте `scripts/deploy-back.sh` есть переменная `REPLICAS=1`, надо изменить ее значение
и затем задеплоить новую версию
