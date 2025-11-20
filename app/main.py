from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import db
from app.routers import skel_router
from app.services.skel_service import SkelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = db.connect()
    SkelService(connection).create_table()
    yield
    db.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skel_router)


@app.get("/", tags=["health"])
def root():
    return {"msg": "yaya", "ver": settings.app_version}


@app.get("/health", tags=["health"])
def health():
    return {"stat": 1, "ver": settings.app_version}
