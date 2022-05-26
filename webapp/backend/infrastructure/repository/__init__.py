#!/usr/bin/env python
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    "postgresql://webapp_postgres_user:webapp_postgres_password@webapp-postgres:5432/webapp_postgres_db"
)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_session():
    """
    Get a session for persistence and retrieval.

    :return: Session
    """
    session = Session()

    return session


def transaction(function):
    @wraps(function)
    def get_session_for_transaction(*args, **kwargs):
        session = get_session()
        try:
            result = function(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return get_session_for_transaction


Base = declarative_base()


def create_all():
    """
    Create database tables.
    """
    Base.metadata.create_all(engine)
