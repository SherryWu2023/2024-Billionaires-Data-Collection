
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from webdriver_manager.chrome import ChromeDriverManager

class Forbes2024Spider(scrapy.Spider):
    name = "forbes2024"
    start_urls = ['https://www.forbes.com/billionaires/']  # replace wi

    def __init__(self):
        # Set up the Selenium driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            # Wait for the table rows to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Table_tableRow__lF_cY'))
            )

            
            sel = Selector(text=self.driver.page_source)
            for row in sel.css('div.Table_tableRow__lF_cY'):
                yield {
                    'rank': row.css('div.Table_rank__X4MKf::text').get(),
                    'name': row.css('div.Table_personName__Bus2E::text').get(),
                    'net_worth': row.css('div.Table_finalWorth__UZA6k span::text').get(),
                    'age': row.css('div:nth-child(4)::text').get(),  
                    'country': row.css('div:nth-child(5)::text').get(),  
                    'source': row.css('div:nth-child(6)::text').get(),  
                    'industry': row.css('div:nth-child(7)::text').get(),  
                }

            # Check if there is a next page button and click it
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
                if "disabled" in next_button.get_attribute("class"):
                    break  
                next_button.click()
            except:
                break  

    def closed(self, reason):
        self.driver.quit()
