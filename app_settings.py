import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE = 'bot_history'
HOST = 'localhost'
USER = 'root'
PASSWORD = 'random'
