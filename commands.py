from discord.ext import commands

def setup_commands(bot):
    @bot.command()
    async def test(ctx):
        """Simple test command to check bot functionality."""
        await ctx.send("Bot is running!")


