import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.messages = True  # Enable MESSAGE_CONTENT intent

discord_bot = commands.Bot(command_prefix='-', intents=intents)
