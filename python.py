import time
import random
import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import logging

# Configure logging to file
logging.basicConfig(filename='background_script.log', level=logging.INFO)

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

    driver = webdriver.Edge(options=options)
    driver.set_window_position(-10000, -10000)  # Move browser window off-screen

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
