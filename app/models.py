from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///local.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    url = Column(String)
    path = Column(String)
    status = Column(Integer)
    duration_ms = Column(Float)


def create_db():
    Base.metadata.create_all(bind=engine)
