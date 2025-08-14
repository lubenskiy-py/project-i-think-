import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
ngrok_token = os.getenv("NGROK_TOKEN")
