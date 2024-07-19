import discord
from discord.ext import commands
from pathlib import Path
import os, dotenv
import logging

from discord_bot.message_format import message_format

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

# Load environment variables from .env file
env_path = Path('.') / '.env'
if env_path.exists():
    dotenv.load_dotenv(dotenv_path=env_path)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

@bot.event
async def on_ready():
    message = f"Logged in as {bot.user} running together with FastAPI!"
    print(message)
    await send_message([message])

async def send_message(messages: list, **kwargs):
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    if channel is None:
        logging.error(f"Failed to find channel with ID {DISCORD_CHANNEL_ID}")
        return
    
    for message in messages:
        try:
            message = message_format(message, kwargs)
            # print(message)
            await channel.send(f"```ansi\n{message}\n```")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

async def run():
    if DISCORD_BOT_TOKEN:
        try:
            await bot.start(DISCORD_BOT_TOKEN)
        except KeyboardInterrupt:
            await bot.logout()
    else:
        logging.error("DISCORD_BOT_TOKEN is not set. Please set the DISCORD_BOT_TOKEN environment variable.")