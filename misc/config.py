import json
import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = json.loads(os.getenv('ADMINS'))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
