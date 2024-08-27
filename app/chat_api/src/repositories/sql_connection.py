from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlite3 import Connection as SQLite3Connection
from config.app_config import config
from functools import wraps
from utilities.logger import logger


DB_URL = config.DB_URL
if DB_URL:
    engine = create_engine(DB_URL)

# Models base class
BaseModel = declarative_base()


def create_db_session():
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    )
    return db_session


def with_db_session(f):
    """
    Decorator that provide the decorated function with a unique db session instance.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        db_session = create_db_session()
        try:
            result = f(*args, db_session=db_session, **kwargs)
            return result
        except Exception as ex:
            logger.exception(str(ex))
            raise
        finally:
            db_session.close()
    return wrapper


@event.listens_for(Engine, "connect")   # Enables sqlite foreign keys constraints
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def init_db():

    # import sql models here to create they tables
    from models.user_models import UserSQLModel
    from models.chat_models import Chat
    from models.chat_member_models import ChatMember
    from models.message_models import Message
    BaseModel.metadata.create_all(bind=engine)
