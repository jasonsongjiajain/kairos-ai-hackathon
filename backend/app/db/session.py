from sqlalchemy.orm import Session, sessionmaker

from app.db.engine import get_engine

SessionLocal = sessionmaker(bind=get_engine(), class_=Session, expire_on_commit=False)


def get_session():
    with SessionLocal() as session:
        yield session
