import os 

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get('client_id')
CLIENT_SECRET = os.environ.get('client_secret')

if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError("CLIENT_ID o CLIENT_SECRET no están definidos en el archivo .env")