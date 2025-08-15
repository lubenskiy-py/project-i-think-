from fastapi import HTTPException, status
from jose import JWTError, jwt

from load_env import secret_key



def decode_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except JWTError:
        return None


def check_role(token):
    current_token = decode_token(token)
    if current_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return current_token["role"]


def is_user(token):
    if check_role(token) != "USER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")


def is_admin(token):
    if check_role(token) != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")
