from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dependencies import get_db
from models import User, Item
from schemas import UserCreate, UserLogin, ItemCreate

import uuid
import os

app = FastAPI()
UPLOAD_DIRECTORY = 'uploaded_images'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_current_user(credentials: HTTPAuthorizationCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == credentials.credentials).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid authorization credentials.')

    return user


@app.post('/register', response_model=UserCreate)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='User already registred.')

    hashed_password = pwd_context.hash(user.password)
    token = str(uuid.uuid4())
    db_user = User(
        username=user.username,
        email=str(user.email),
        hashed_password=hashed_password,
        token=token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {'message': 'User created.', 'token': token}


@app.post('/login')
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail='Invalid email.')

    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid password.')

    return {'message': 'Login successful.', 'token': db_user.token}


@app.post('/items')
async def create_item(
        item: ItemCreate,
        file: UploadFile = File(default=None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    image_path = None

    if file:
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

        with open(file_path, 'wb') as buffer:
            buffer.write(file.file.read())

        image_path = file_path

    new_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
        category=item.category,
        user_id=current_user.id,
        image_path=image_path
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {'message': 'Item created successfully', 'item': new_item}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
