import asyncio
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from config import BETALAND_USERNAME, BETALAND_PASSWORD, DISCORD_CHANNEL_ID
from discord_bot import send_to_discord
from utils import print_error, print_info, print_success, print_warning
import csv

def switch_to_window_by_title(driver, title):
    """Switches to the window that matches the given title."""
    try:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            print_info(f"Checking window with title: {driver.title}")
            if title in driver.title:
                print_success(f"Switched to window: {driver.title}")
                return True
        return False
    except Exception as e:
        print_error(f"Failed to switch window: {e}")
        return False
        
def switch_to_iframe(driver, iframe_id):
    """Switches to the iframe using the given iframe_id."""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, iframe_id)))
        driver.switch_to.frame(driver.find_element(By.ID, iframe_id))
    except Exception as e:
        print_error(f"Error switching to iframe: {e}")

def open_betaland(driver):
    """Navigates to the Betaland Poker page."""
    driver.get("https://www.betaland.it/poker")
    time.sleep(3)
    print_success("Opened Betaland Poker page.")
    
def login(driver, username, password):
    """Logs into Betaland."""
    try:
        driver.find_element(By.ID, "cg-username").send_keys(username)
        driver.find_element(By.ID, "cg-password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "bottone-login").click()
        print_success("Login successful.")
    except Exception as e:
        print_error(f"Login failed: {e}")
        
def click_velox_and_observe(driver):
    """Click the Velox tab and select the Observe filter."""
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@for='UNIQUE-144']"))
        ).click()
        print_success("Clicked on Velox tab.")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@for='UNIQUE-211' and contains(text(), 'Osserva')]"))
        ).click()
        print_success("Selected 'Observe' option.")
    except Exception as e:
        print_error(f"Error selecting Observe: {e}")

def play_online(driver):
    """Opens the People's Poker Client."""
    try:
        driver.find_element(By.XPATH, "//a[contains(@class, 'pointer') and contains(text(), 'Gioca')]").click()
        print_success("Clicked 'Gioca'.")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        time.sleep(5)
        for window in driver.window_handles:
            driver.switch_to.window(window)
            if "People's Poker Client" in driver.title:
                print_success(f"Switched to: {driver.title}")
                return window
        print_error("Poker Client window not found.")
        return None
    except Exception as e:
        print_error(f"Error opening Poker Client: {e}")
        return None

def click_osserva_button(driver, amount_text):
    """Clicks 'Osserva' and switches to the game window."""
    try:
        time.sleep(2)
        items = driver.find_elements(By.CSS_SELECTOR, "item[ng-repeat='id in visibleItems']")
        if items:
            print_info("Items are present, proceeding with element lookup.")
        for index, item in enumerate(items):
            try:
                name_text = item.find_element(By.XPATH, ".//span[contains(@class, 'name ng-binding')]").get_attribute("textContent").strip()
                amount_value = item.find_element(By.XPATH, ".//span[contains(@class, 'ng-binding') and not(contains(@class, 'name'))]").get_attribute("textContent").strip()
                print_info(f"Checking item {index + 1}: {name_text} {amount_value}")
                if name_text == "VeloX 3Max da" and amount_value == f"€{amount_text}":
                    osserva_buttons = item.find_elements(By.XPATH, ".//button[contains(@class, 'ng-binding') and contains(text(), 'Osserva')]")
                    osserva_button = osserva_buttons[1] if len(osserva_buttons) >= 2 else osserva_buttons[0]
                    driver.execute_script("arguments[0].click();", osserva_button)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(osserva_button))
                    ActionChains(driver).move_to_element(osserva_button).click().perform()
                    print_success(f"Clicked 'Osserva' for: {name_text} {amount_value}")
                    time.sleep(10)
                    return switch_to_window_by_title(driver, f"da 3 Giocatori da {amount_text.replace('.', ',')}€")
            except Exception as e:
                print_error(f"Error processing item {index + 1}: {e}")
        print_warning(f"No matching table for €{amount_text}")
        return False
    except Exception as e:
        print_error(f"General error: {str(e)}")
        return False
    
def click_home_button(driver):
    """Clicks the 'Home' button on the page."""
    try:
        home_button = driver.find_element(By.XPATH, '//button[@action="home"]')
        home_button.click()
        print_success("Home button clicked successfully!")
        
    except Exception as e:
        print_error(f"Error clicking 'Home' button: {e}")
        
def tournament_id_exists(csv_file_path, tournament_id):
    """Check if the tournament ID already exists in the CSV file."""
    if not os.path.exists(csv_file_path):
        return False

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == tournament_id:  # Assuming the tournament ID is in the first column
                return True
    return False

def append_tournament_id_to_csv(csv_file_path, tournament_id):
    """Append the tournament ID to the CSV file."""
    file_exists = os.path.exists(csv_file_path)
    
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['Tournament ID'])  # Write header if the file is new
        writer.writerow([tournament_id])  # Add the tournament ID to the CSV

async def retrieve_table_data(driver, stake):
    """Retrieves the data of the current table, sends it to Discord, and closes windows safely."""
    table_window = None
    latest_window_handle = None
    csv_file_path = 'tournaments.csv'
    try:
        table_window = driver.current_window_handle
        click_home_button(driver)
        time.sleep(2)
        
        # Ensure that a new window is opened
        if len(driver.window_handles) < 2:
            print_info("No new window detected.")
            return None
        
        latest_window_handle = driver.window_handles[-1]
        driver.switch_to.window(latest_window_handle)
        
        # Click on 'Giocatori' button
        try:
            giocatori_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@ng-click=\"panel = 'players'\"]"))
            )
            giocatori_button.click()
            print_info("Clicked on 'Giocatori' button.")
        except Exception as e:
            print_error(f"Error clicking 'Giocatori' button: {e}")
            return None
        
        # Click on 'Lista Giocatori' button
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Lista Giocatori')]"))
            )
            button.click()
            print_info("Clicked on 'Lista Giocatori' button.")
        except Exception as e:
            print_error(f"Error clicking 'Lista Giocatori' button: {e}")
            return None
        
        time.sleep(2)

        # Retrieve player names
        try:
            player_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'tableListRowTextual')]//label[@class='name ng-binding ng-scope']")
            # Use a set to automatically remove duplicates
            player_names = set()
            for element in player_elements:
                name = element.text.strip()  # Remove leading/trailing spaces
                if name:  # Ensure the name is not empty
                    player_names.add(name)
            player_names = list(player_names)  # Convert set back to list to remove duplicates
        except Exception as e:
            print_error(f"Error retrieving player names: {e}")
            player_names = []

        # Retrieve tournament ID
        try:
            tournament_id_element = driver.find_element(By.CSS_SELECTOR, "tournament-id.ng-binding")
            tournament_id = tournament_id_element.text.strip().split(":")[-1].strip()
        except Exception as e:
            print_error(f"Error retrieving tournament ID: {e}")
            tournament_id = "Unknown"
            
        if tournament_id_exists(csv_file_path, tournament_id):
            print_warning(f"Tournament ID {tournament_id} already exists. No message sent.")
            return None
        
        # If the tournament ID doesn't exist, add it to the CSV
        append_tournament_id_to_csv(csv_file_path, tournament_id)

        # Prepare table data
        table_data = {
            "players": player_names,
            "tournament_id": tournament_id,
            "stake": f'€{stake}'
        }

        # Prepare message for Discord
        message =  f"\n**Stake:** €{stake}" + f"\n**Tournament ID:** {tournament_id}\n**Players:**\n" + "\n".join(player_names) if player_names else "**No players found.**"

        await send_to_discord(int(DISCORD_CHANNEL_ID), message)

        return table_data

    except Exception as e:
        print_error(f"Error retrieving table data: {e}")
        return None

    finally:
        # Ensure proper window closure even if an error occurs
        if latest_window_handle and latest_window_handle in driver.window_handles:
            driver.close()
            print_info("Closed latest game window.")

        if table_window and table_window in driver.window_handles:
            driver.switch_to.window(table_window)
            driver.close()
            print_info("Closed original game window.")
    
async def observe_game(driver, button):
    """Helper function to observe the game for a given button."""
    try:
        if click_osserva_button(driver, button):
            print_success(f"Observing game with button {button}...")
            await asyncio.sleep(5)
            await retrieve_table_data(driver, button)
            driver.switch_to.window(poker_client_handle)
            print_success("Back to Poker Client.")
            return None
        else:
            print_warning(f"No game found with buy in €{button}.")
            return None
    except Exception as e:
        print_error(f"Error observing game with button {button}: {e}")
        driver.switch_to.window(poker_client_handle)
        return False

    
async def run_browser_scraping(driver):
    """Runs the bot to observe games."""
    open_betaland(driver)
    login(driver, BETALAND_USERNAME, BETALAND_PASSWORD)
    await asyncio.sleep(10)
    global poker_client_handle
    poker_client_handle = play_online(driver)
    switch_to_iframe(driver, "poker-frame")
    click_velox_and_observe(driver)
    await asyncio.sleep(2)

    cycle_counter = 0  # Counter to alternate between buttons

    while True:
        if driver.find_elements(By.ID, "poker-frame"):
            print_info("Switching to Poker Client iframe...")
            switch_to_iframe(driver, "poker-frame")

        print_info("Checking for possible running games...")
        # Alternate between "50" and "100" using cycle_counter
        button_to_click = "100" if cycle_counter % 2 == 0 else "50"
        await observe_game(driver, button_to_click)
        cycle_counter += 1

        print_warning("Retrying in 5s...")
        await asyncio.sleep(5)

