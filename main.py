import asyncio
import os
import sys
from browser_bot import run_browser_scraping
from config import TOKEN
from selenium_setup import setup_selenium
from discord_bot import discord_bot

async def restart_application():
    """Closes the WebDriver and restarts the application every 59 minutes."""
    await asyncio.sleep(3540)  # 59 minutes
    print("Restarting application...")

    # Shutdown WebDriver
    try:
        driver.quit()
        print("WebDriver closed successfully.")
    except Exception as e:
        print(f"Error closing WebDriver: {e}")

    # Shutdown Discord bot
    try:
        await discord_bot.close()
        print("Discord bot shut down successfully.")
    except Exception as e:
        print(f"Error shutting down Discord bot: {e}")

    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)  # Replace current process with new instance

@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user}")

    # Start Selenium WebDriver
    try:
        global driver  # Ensure the driver can be accessed in restart function
        driver = setup_selenium()
        print("Selenium WebDriver initialized successfully.")

        # Run browser scraping
        discord_bot.loop.create_task(start_browser_scraping(driver))

        # Start restart loop
        discord_bot.loop.create_task(restart_application())

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        sys.exit(1)

async def start_browser_scraping(driver):
    try:
        await run_browser_scraping(driver)
    except Exception as e:
        print(f"Error running browser scraping: {e}")

async def main():
    while True:  # Ensures script restarts after failure
        if TOKEN:
            try:
                await discord_bot.start(TOKEN)
            except Exception as e:
                print(f"Error starting bot: {e}")
            finally:
                print("Bot stopped. Restarting in 5 seconds...")
                await asyncio.sleep(5)  # Small delay before restart
        else:
            print("Discord token is missing. Set it in a .env file.")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
