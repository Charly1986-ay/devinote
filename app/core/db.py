
import os
from typing import Iterator
from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

raw_url = os.environ('DATABASE_URL')

if raw_url.startswith('postgres://'):
    raw_url = 'postgresql+psycopg://' + raw_url[len('postgres://'):]
elif raw_url.startswith('postgres://') and '+psycopg' not in raw_url:
    raw_url = 'postgresql+psycopg://' + raw_url[len('postgresql://'):]


# engine = create_engine(settings.DATABASE_URL, echo=False, connect_args={
#                        "check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
engine = create_engine(raw_url, pool_pre_ping=True)

def init_db() -> None:
    if settings.ENVIRONMENT=='DEV':
        SQLModel.metadata.create_all(engine)  # dev


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
