from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import re

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    # Add more User-Agent strings as needed
]

# Setup Chrome options
base_options = Options()
base_options.add_argument("--headless")  # Run headlessly
base_options.add_argument("--no-sandbox")
base_options.add_argument("--disable-dev-shm-usage")
base_options.add_argument("--window-size=1920,1080")  # Set window size
base_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flags

class Scraper:
    def __init__(self):
        return

    def get(self, url):
        time.sleep(random.uniform(1, 3))  # Random delay
        chrome_options = base_options
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(page_source, 'html.parser')
        if re.compile(r'\bCloudflare\b').search(str(soup.title)):
            print('Cloudflare detected.')
            return ''
        return page_source
