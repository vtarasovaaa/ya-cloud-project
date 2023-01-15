import uvicorn
from fastapi import APIRouter, FastAPI

from views.note import get_notes, save_note
from views.version import get_app_version


def create_app():
    app = FastAPI()

    router = APIRouter()
    router.add_api_route('/version', get_app_version, methods=['GET'])
    router.add_api_route('/notes', get_notes, methods=['GET'])
    router.add_api_route('/note', save_note, methods=['POST'])

    app.include_router(router)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=8080)
