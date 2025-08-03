import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from init_db import engine
from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def decode_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except JWTError:
        return None

# def is_admin(token):
#     check_token = decode_token(token)
#     if check_token is None:
#
#     if check_token["role"] != "ADMIN":
#         return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
