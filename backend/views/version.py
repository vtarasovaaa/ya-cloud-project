import platform
from functools import cache

import fastapi
import requests
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    version: str

    os_url: str = 'https://storage.yandexcloud.net/ya-cloud-project-notes-vtarasovaaa/index.html'
    auth_token: str

    class Config:
        env_prefix = 'APP_'


@cache
def get_settings() -> AppSettings:
    return AppSettings()


def get_app_version(settings: AppSettings = fastapi.Depends(get_settings)):
    response = requests.get(settings.os_url, headers={'Authorization': settings.auth_token})
    return {
        'version': settings.version,
        'name': platform.node(),
        'front_version': response.headers.get('x-amz-version-id'),
    }
