from email.policy import default

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

# def is_admin(token):
#     current_token = decode_token(token)
#     if current_token is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
#     if current_token["role"] != "ADMIN":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")
#     return True

"""
def validate_image(filename: str, content: bytes):
    ext = filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise ValueError(f"Unsupported file extension: {ext}. Supported formats are JPG, JPEG, PNG.")
    
    if not content:
        raise ValueError("File content is empty")
    
    if len(content) > 5 * 1024 * 1024:
        raise ValueError("File size exceeds 5MB limit")

    try:
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        raise ValueError(f"Invalid image file: {filename}")


try:
    validate_image(file.filename, content)
except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
"""