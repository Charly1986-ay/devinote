from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth_router, labels_router, notes_router, shares_router
from app.core.config import settings
from app.core.db import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    swagger_ui_parameters= {
        'persistAuthorization': True
    }
)

app.add_middleware(
    CORSMiddleware,
    # en desarrollo se pone asi, en produccion se cambia
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router.router, prefix='/api/v1')
app.include_router(notes_router.router, prefix='/api/v1')
app.include_router(labels_router.router, prefix='/api/v1')
app.include_router(shares_router.router, prefix='/api/v1')