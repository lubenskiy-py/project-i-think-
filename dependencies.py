import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker
from init_db import engine
from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
