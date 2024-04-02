from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlite3 import Connection as SQLite3Connection
from utilities.utils import get_env_value
from dotenv import load_dotenv


# Models base class
BaseModel = declarative_base()
engine = None
db_session = None


def get_engine():
    global engine
    if engine is None:
        load_dotenv()
        DB_URL = get_env_value("DB_URL")
        engine = create_engine(DB_URL)
    return engine


def get_db_session():
    global db_session
    if db_session is None:
        engine = get_engine()
        db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
    return db_session


@event.listens_for(Engine, "connect")   # Enables sqlite foreign keys constraints
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def init_db():

    engine = get_engine()
    db_session = get_db_session()
    BaseModel.query = db_session.query_property()   # allows starting queries using the session without needing to reference the session explicitly

    # import sql models here to create they tables
    from models.user_models import UserSQLModel
    from models.contact_models import Contact
    from models.chat_models import Chat
    from models.chat_member_models import ChatMember
    from models.message_models import Message
    BaseModel.metadata.create_all(bind=engine)
