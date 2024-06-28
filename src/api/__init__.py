from fastapi import FastAPI
from .routes import configure_routes


def create_app():
    app = FastAPI()
    configure_routes(app)
    return app
