from browser_bot import run_browser_scraping
from config import TOKEN
from selenium_setup import setup_selenium
from discord_bot import discord_bot
from commands import setup_commands
import sys

# Initialize Selenium WebDriver
try:
    driver = setup_selenium()
    print("Selenium WebDriver initialized successfully.")
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    driver = None
    sys.exit(1)

# Load bot commands
setup_commands(discord_bot)

# Start browser automation steps
run_browser_scraping(driver)

@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user}")

if TOKEN:
    try:
        discord_bot.run(TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
    finally:
        if driver:
            driver.quit()
            print("Selenium WebDriver closed.")
else:
    print("Discord token is missing. Set it in a .env file.")

print("Bot finished running.")
