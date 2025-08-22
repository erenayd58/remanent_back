
from sqlmodel import SQLModel, create_engine, Session
from .settings import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=False)

def init_db():
    from . import models  # noqa
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
