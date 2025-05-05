import os

from asyncio import get_event_loop
from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from data_base_sql import sql_commands


load_dotenv()

TOKEN = os.getenv('TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')
DATABASE_LINK = os.getenv('DATABASE_LINK')

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

db_admins = sql_commands.AdminCommands()
db_clients = sql_commands.ClientCommands()
