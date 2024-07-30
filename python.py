import time
import random
import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import logging
import tkinter as tk

# Configure logging to file
logging.basicConfig(filename='background_script.log', level=logging.INFO)

# List of common user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"
]

# List of common referrer URLs
referrers = [
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://www.instagram.com/",
    "https://www.twitter.com/",
    "https://www.linkedin.com/",
    "https://www.pinterest.com/",
    "https://www.reddit.com/",
    "https://www.tumblr.com/",
    "https://www.quora.com/",
    "https://www.snapchat.com/",
    "https://www.medium.com/",
    "https://www.whatsapp.com/",
    "https://www.wechat.com/",
    "https://www.yahoo.com/",
    "https://www.bing.com/",
    "https://www.duckduckgo.com/",
    "https://www.yandex.com/"
]

def download_edge_driver():
    edge_version = os.popen('wmic datafile where name="C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe" get Version /value').read()
    edge_version = edge_version.strip().split("=")[-1]
    major_version = edge_version.split('.')[0]
    
    logging.info(f"Detected Edge version: {edge_version}")

    driver_url = f"https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win64.zip"
    
    response = requests.get(driver_url, stream=True)
    if response.status_code == 200:
        with open('edgedriver.zip', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        with zipfile.ZipFile('edgedriver.zip', 'r') as zip_ref:
            zip_ref.extractall()

        os.remove('edgedriver.zip')
        
        logging.info("Edge WebDriver downloaded and extracted successfully.")
    else:
        logging.error("Failed to download Edge WebDriver. Please check your internet connection or Edge version.")

def setup_driver():
    if not os.path.exists('msedgedriver.exe'):
        download_edge_driver()

    options = Options()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Disable sandboxing for better performance

    # Randomly select a user agent
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Edge(options=options)
    driver.set_window_position(-10000, -10000)  # Move browser window off-screen
    # Get screen size using tkinter
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # Set window size to match screen size
    driver.set_window_size(screen_width, screen_height)

    return driver

def get_random_page(driver, base_url):
    driver.get(base_url)
    time.sleep(2)
    
    links = driver.find_elements(By.TAG_NAME, 'a')
    valid_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and base_url in link.get_attribute('href')]
    
    if valid_links:
        return random.choice(valid_links)
    else:
        return base_url

def visit_website(base_url):
    driver = setup_driver()

    try:
        while True:
            random_page = get_random_page(driver, base_url)
            
            # Randomly select a referrer
            referrer = random.choice(referrers)
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Referer': referrer}})
            
            driver.get(random_page)

            time.sleep(2)

            scroll_pause_time = 45
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            step = scroll_height / scroll_pause_time

            for i in range(scroll_pause_time):
                driver.execute_script(f"window.scrollBy(0, {step});")
                time.sleep(1)

            driver.execute_script("window.scrollTo(0, 0);")

            delay = random.uniform(15, 60)
            logging.info(f"Reloading the page in {delay:.2f} seconds...")
            time.sleep(delay)
    finally:
        driver.quit()

def main():
    base_url = "https://blogspotyteam.blogspot.com/"
    visit_website(base_url)

if __name__ == "__main__":
    main()

    # pyinstaller --onefile --noconsole python.py