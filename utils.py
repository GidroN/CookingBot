import os
import json
from dotenv import load_dotenv
from keyboards.reply import main_menu_user_kb

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = json.loads(os.getenv('ADMINS'))


def is_admin(tg_id: str) -> bool:
    return tg_id in ADMINS


def get_main_kb(tg_id: str):
    return main_menu_user_kb
