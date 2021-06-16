import datetime
import pandas as pd
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class NewsVolumeScraper:
    def __init__(self, ticker):
        self.ticker = ticker
        self.error = 0
        self.data = {}
        self.data['volume'] = []
        self.data['date'] = []
        
        
    def get_data(self):
        return self.data
        
    def scrape(self, start_date, end_date):
        validate(start_date)
        validate(end_date)
        
        date_range = pd.date_range(start=start_date, end=end_date).strftime('%m/%d/%Y')
        
        for i in range(0, len(date_range), 30):
            
            if self.error == 3:
                print('Probably identified as a bot. Aborting...')
                break
            
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.implicitly_wait(2)
            
            dates = date_range[i:i+30]
            
            for date in dates:
                news_volume = self.get_news_volume(driver, date)
                self.data['volume'].append(news_volume)
                self.data['date'].append(date)
                
            driver.quit()
                    
        
    def get_news_volume(self, driver, date):
        search_url = 'https://www.google.com/search?q={0}&tbs=cdr:1,cd_min:{1},cd_max:{1}&tbm=nws'.format(self.ticker, date)
        time.sleep(random.uniform(0.2, 1.0))
        driver.get(search_url)
        self.accept_cookies(driver)
        
        news_volume = None
        
        print('Getting news volume for {}'.format(date))
        try:
            news_vol = driver.find_element_by_id('result-stats').get_attribute('innerHTML')
            news_vol = news_vol.replace('.', '')
            news_vol = news_vol.split('<')[0]
            news_volume = [int(s) for s in news_vol.split() if s.isdigit()][0]
            
            if self.error > 0: self.error -= 1
    
        except NoSuchElementException:
            print('Could not find element for {}.'.format(date))
            self.error += 3
            
        return news_volume
        
    def accept_cookies(self, driver):
        try:
            button = driver.find_element(By.TAG_NAME, 'button')
            if button.text.lower() == 'ik ga akkoord':
                button.click()
        except ValueError as v:
            raise('Something went wrong while accepting cookies.{}'.format(v)) 
        
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be MM/DD/YYYY")
