from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from political_credibility.common.settings import get_settings


def build_session_factory() -> sessionmaker:
    engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

