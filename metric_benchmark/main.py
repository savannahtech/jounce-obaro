from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import settings_config
from metric_benchmark.apis.base import api_router


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(
        title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION
    )
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_router(app)
    return app


app = start_application()


@app.get("/healthz")
def read_root():
    # This endpoint is used to check the health of the application
    return {"message": "success"}
