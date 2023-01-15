#!/bin/bash

if [[ -z $1 ]];
then
    echo -n "Enter new backend version: "
    read TAG
else
    TAG=$1
fi

IMAGE_NAME=cr.yandex/crpjbulf5ghieq1vv9hn/ya-cloud-project-back:$TAG
SERVICE_ACCOUNT_ID=$SERVICE_ACCOUNT_ID
FOLDER_ID=$FOLDER_ID
NOTE_STORAGE_DATABASE=$YDB_DATABASE
NOTE_STORAGE_ENDPOINT=$YDB_ENDPOINT
APP_AUTH_TOKEN=$SECRET_KEY

REPLICAS=1

docker build backend -t $IMAGE_NAME
docker push $IMAGE_NAME
yc serverless container revision deploy \
  --container-name ya-cloud-project-vtarasovaaa-container \
  --image $IMAGE_NAME \
  --min-instances $REPLICAS \
  --cores 1 \
  --memory 1GB \
  --concurrency 1 \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --execution-timeout 30s \
  --folder-id $FOLDER_ID \
  --environment NOTE_STORAGE_DATABASE=$NOTE_STORAGE_DATABASE,NOTE_STORAGE_ENDPOINT=$NOTE_STORAGE_ENDPOINT,USE_METADATA_CREDENTIALS=1,APP_VERSION=$TAG,APP_AUTH_TOKEN=$APP_AUTH_TOKEN
