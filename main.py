import asyncio
from browser_bot import run_browser_scraping
from config import TOKEN
import discord_bot
from selenium_setup import setup_selenium
import sys

@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user}")
    # Start browser scraping when bot is ready
    try:
        driver = setup_selenium()
        print("Selenium WebDriver initialized successfully.")
        # Run browser scraping asynchronously
        discord_bot.loop.create_task(start_browser_scraping(driver))
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        sys.exit(1)

async def start_browser_scraping(driver):
    try:
        await run_browser_scraping(driver)
    except Exception as e:
        print(f"Error running browser scraping: {e}")

async def main():
    if TOKEN:
        try:
            await discord_bot.start(TOKEN)
        except Exception as e:
            print(f"Error starting bot: {e}")
        finally:
            print("Bot finished running.")
    else:
        print("Discord token is missing. Set it in a .env file.")

if __name__ == "__main__":
    # Call main() directly, but use discord_bot.start() inside it
    asyncio.run(main())
