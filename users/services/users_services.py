from fastapi import HTTPException, status
from jose import jwt

from users.db.models import User
from load_env import secret_key
from users.schemas.schemas import CreateUser



async def register(user, db):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registred.')

    data = CreateUser(**user.model_dump())
    token = jwt.encode(data.model_dump(), secret_key, algorithm='HS256')

    db_user = User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return token
