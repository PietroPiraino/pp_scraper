from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_selenium():
    """Initializes Selenium WebDriver with anti-detection settings."""
    # Automatically get the correct version of Chromedriver
    service = Service(ChromeDriverManager().install())  # Uses webdriver-manager to handle the driver installation
    options = webdriver.ChromeOptions()
    
    # Use a standard user-agent and disable automation features
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled" message
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--start-maximized")  # Start Chrome maximized
    # options.add_argument("--headless")  # Run Chrome in headless mode if you don't need UI (optional)
    options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    
    # For advanced browser manipulation to hide "webdriver"
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
     # 🚀 Disable "Save Password" popups
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Modify navigator.webdriver to avoid detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver
