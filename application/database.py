import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///local.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

def init_db():
    from .sentences import models

    Base.metadata.create_all(bind=engine)