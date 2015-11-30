from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from photoblaster.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


engine = create_engine('mysql://{}:{}@{}/{}'.format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME
))

session_factory = sessionmaker(bind=engine)
SessionHeap = scoped_session(session_factory)
