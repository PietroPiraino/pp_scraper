import discord
from discord.ext import commands

from utils import print_error, print_success

intents = discord.Intents.all()
intents.members = True
intents.messages = True

discord_bot = commands.Bot(command_prefix='-', intents=intents)

async def send_to_discord(channel_id: int, message: str):
    """Sends a message to a specific Discord channel."""
    channel = discord_bot.get_channel(channel_id)
    
    embed_description = message
    embed = discord.Embed(description=embed_description, colour=discord.Colour.green())
    
    if channel:
        print_success(f"Sending message to channel {channel_id}: {message}")
        await channel.send(embed=embed)
    else:
        print_error(f"Channel with ID {channel_id} not found.")
        
    return None