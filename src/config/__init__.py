from dotenv import dotenv_values
from telethon import TelegramClient

# Importante valores do dotenv
APP_ID: int = dotenv_values()["APP_ID"]
API_HASH: str = dotenv_values()["API_HASH"]
BOT_TOKEN: str = dotenv_values()["BOT_TOKEN"]
BOT_NAME: str = dotenv_values()["BOT_NAME"]
SUPPORT_CHANNEL_GERAL: int = dotenv_values()["SUPPORT_CHANNEL_GERAL"]
SUPPORT_CHANNEL_VENDAS: int = dotenv_values()["SUPPORT_CHANNEL_VENDAS"]
SUPPORT_CHANNEL_CONTATO: int = dotenv_values()["SUPPORT_CHANNEL_CONTATO"]

BASE_URL_API: str = dotenv_values()["BASE_URL_API"]

BOT = TelegramClient(BOT_NAME, APP_ID, API_HASH)
BOT.parse_mode = "md"
