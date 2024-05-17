import os
import json
import re

from dotenv import load_dotenv
from keyboards.reply import main_menu_user_kb

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = json.loads(os.getenv('ADMINS'))


def is_admin(tg_id: str) -> bool:
    return tg_id in ADMINS


def get_main_kb(tg_id: int):
    return main_menu_user_kb


def extract_recipe_info(text):
    lines = text.strip().split('\n')

    name_line = lines[0].strip()
    url_line = lines[1].strip()

    name_match = re.match(r"^\d+\)\s*(.+)", name_line)
    name = name_match.group(1) if name_match else None

    url_match = re.match(r"^\d+\)\s*(https?://[^\s]+)", url_line)
    url = url_match.group(1) if url_match else None

    return name, url
