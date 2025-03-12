from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from config import BETALAND_USERNAME, BETALAND_PASSWORD

def switch_to_window_by_title(driver, title):
    """Switches to the window that matches the given title."""
    window_handles = driver.window_handles
    for handle in window_handles:
        driver.switch_to.window(handle)
        print(f"Checking window with title: {driver.title}")
        if title in driver.title:  # Match part of the title or the entire title
            print(f"Switched to the window with title: {driver.title}")
            return True
    return False

def switch_to_iframe(driver, iframe_id):
    """Switches to the iframe using the given iframe_id."""
    try:
        # Wait for the iframe to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, iframe_id)))
        
        # Switch to the iframe
        iframe = driver.find_element(By.ID, iframe_id)
        driver.switch_to.frame(iframe)
        print(f"Switched to iframe with ID: {iframe_id}")
    except Exception as e:
        print(f"Error switching to iframe: {e}")

def open_betaland(driver):
    """Navigates to the Betaland Poker page."""
    driver.get("https://www.betaland.it/poker")
    time.sleep(3)  # Wait for the page to load

def login(driver, username, password):
    """Logs into Betaland using provided credentials."""
    try:
        username_input = driver.find_element(By.ID, "cg-username")
        password_input = driver.find_element(By.ID, "cg-password")
        login_button = driver.find_element(By.CLASS_NAME, "bottone-login")

        username_input.send_keys(username)
        password_input.send_keys(password)
        time.sleep(1)  # Wait for the inputs to be filled
        login_button.click()

        print("Login successful.")
    except Exception as e:
        print(f"Login failed: {e}")
        
def click_velox_and_observe(driver):
    """Click the Velox tab and select the Observe filter."""
    try:
        # Wait for the Velox tab to be visible (ignoring ng-hide)
        velox_tab = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@for='UNIQUE-144']"))
        )
        
        # Click the Velox tab
        velox_tab.click()
        print("Clicked on the Velox tab.")
        
        # Wait for the filter options to load and select 'Observe'
        observe_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@for='UNIQUE-211' and contains(text(), 'Osserva')]"))
        )
        
        # Click on the 'Observe' option (assuming it's a selectable label)
        observe_option.click()
        print("Selected the 'Observe' option under Velox.")
        
    except Exception as e:
        print(f"Error interacting with the Velox tab or selecting the Observe filter: {e}")

def play_online(driver):
    """Clicks the 'Gioca' button, waits for the new window with a specific title, and switches to it."""
    try:
        # Locate and click the 'Gioca' button
        play_button = driver.find_element(By.XPATH, "//a[contains(@class, 'pointer') and contains(text(), 'Gioca')]")
        play_button.click()
        print("Clicked the 'Gioca' button to play online.")
        
        # Wait for the new window to appear (maximum 10 seconds)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        time.sleep(10)  # Wait for the new window to load
        
        # Get the title of the new window to wait for
        new_window_title = "People's Poker Client"
        
        # Switch to the new window using its title
        switch_to_window_by_title(driver, new_window_title)
        
    except Exception as e:
        print(f"Error interacting with the 'Gioca' button or switching windows: {e}")


def accept_cookies(driver):
    """Accepts cookies if the popup appears."""
    try:
        cookie_button = driver.find_element(By.ID, "accept-cookies")  # Update with actual ID
        cookie_button.click()
        print("Cookies accepted.")
    except Exception:
        print("No cookie popup found.")

def perform_poker_actions(driver):
    """Performs poker-related actions."""
    try:
        # Example: Click on a poker game
        poker_game = driver.find_element(By.CLASS_NAME, "poker-game-class")  # Update with actual class
        poker_game.click()
        print("Entered poker game.")
    except Exception as e:
        print(f"Error performing poker actions: {e}")

def run_browser_scraping(driver):
    """Runs the browser scraping steps."""
    open_betaland(driver)
    login(driver, BETALAND_USERNAME, BETALAND_PASSWORD)
    time.sleep(5)  # Wait for the login to complete
    play_online(driver)
    switch_to_iframe(driver, "poker-frame")
    click_velox_and_observe(driver)
    # accept_cookies(driver)
    # perform_poker_actions(driver)
    # Add more