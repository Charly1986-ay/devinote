import os
from typing import Iterator
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

# Cargar variables de entorno (LOCAL)
load_dotenv()

# Obtener DATABASE_URL de forma segura
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL no está configurada")

# Fix compatibilidad postgres (opcional pero recomendado)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)


# engine = create_engine(settings.DATABASE_URL, echo=False, connect_args={
#                        "check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db() -> None:
    pass
    """ if settings.ENVIRONMENT=='DEV':
        SQLModel.metadata.create_all(engine)  # dev """


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
