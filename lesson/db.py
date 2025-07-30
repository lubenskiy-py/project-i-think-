from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = 'sqlite:///marketplace.db'
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
