from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import config
from src.db import Base, engine
from src.models import *
from src.routes import _v1

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    servers=[{"url": f"http://127.0.0.1:{config.port}/"}],
    debug=config.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=config.cors_allow_credentials,
    allow_methods=config.cors_allow_methods,
    allow_headers=config.cors_allow_headers,
)

app.include_router(_v1, prefix="/v1")

Base.metadata.create_all(bind=engine, checkfirst=True)


@app.get("/")
async def version():
    """Return the version of the API."""
    return config.version
