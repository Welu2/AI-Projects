from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the local SQLite database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_platform.db"

# 2. Create the engine connection (connect_args is only needed for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a session factory for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a base class that our database tables will inherit from
Base = declarative_base()

# 5. Dependency helper to yield database sessions safely per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
