import ssl

from fastapi import FastAPI

from usl_config import config
from usl_routes.v1.usl import router as usl_v1_router

ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI(
    title='Universal Scammer List REST API',
    description='A REST API for simplifying queries to the Universal Scammer List database.',
    version='1.0',
    openapi_tags=[
        {
            "name": "usl",
            "description": "Operations concerning the Universal Scammer List.",
        },
    ],
    openapi_url='/openapi.json' if config.local_dev else None
)

app.include_router(usl_v1_router)
