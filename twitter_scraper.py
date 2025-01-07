from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
import uuid
import requests

# Configure ProxyMesh
PROXY_URL = "http://username:password@proxy-ip:port"

# MongoDB setup
MONGO_URI = "your_mongodb_uri"
DB_NAME = "twitter_scraper"
COLLECTION_NAME = "trending_topics"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_trending_topics():
    # Selenium setup with Proxy
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={PROXY_URL}")
    chrome_options.add_argument("--headless")  # Run in headless mode if needed
    
    driver_service = Service("path/to/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    try:
        # Log in to Twitter
        driver.get("https://twitter.com/login")
        username = driver.find_element(By.NAME, "session[username_or_email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys("your_twitter_username")
        password.send_keys("your_twitter_password")
        password.send_keys(Keys.RETURN)

        # Wait for page to load and navigate to the home page
        driver.implicitly_wait(10)
        driver.get("https://twitter.com/home")

        # Scrape the top 5 trending topics
        trending_section = driver.find_element(By.XPATH, "//section[contains(@aria-label, 'What’s happening')]")
        trends = trending_section.find_elements(By.XPATH, ".//span[contains(@class, 'css-class-for-trending')]")[:5]
        trending_topics = [trend.text for trend in trends]

        # Fetch IP address used
        ip_address = requests.get("https://api.ipify.org").text

        # Save results to MongoDB
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now()
        record = {
            "_id": unique_id,
            "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
            "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
            "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
            "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
            "trend5": trending_topics[4] if len(trending_topics) > 4 else None,
            "timestamp": timestamp,
            "ip_address": ip_address,
        }
        collection.insert_one(record)

        return record
    finally:
        driver.quit()
