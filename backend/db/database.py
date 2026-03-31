from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,
    connect_args={"check_same_thread": False},
)


# Set journal mode to WAL - enable simultaneous read/write to/from DB
# synchronous=NORMAL required to prevent data corruption
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.fetchone()
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.close()


# Create a base class for our models
Base = declarative_base()

# Create a session factory bound to our engine
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
