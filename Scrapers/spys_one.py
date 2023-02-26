from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import Firefox, ChromiumEdge
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome
from bs4 import BeautifulSoup
import time


class SpysException(Exception):
    pass


class SpysOne(Chrome, By):
    def __init__(self):
        By.__init__(self)

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        options.headless = True

        Chrome.__init__(self, options=options)
        self.maximize_window()

        self.scraped_proxies = []
        self.url = 'https://spys.one/en/free-proxy-list/'

    def load_page(self):
        self.get(self.url)
    
    def select_full_list(self):
        dropdown_ID = 'xpp'
        toolbar_option_xpath = '/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/font/select[1]/option[6]'    

        dropdown = self.find_element(self.ID, dropdown_ID)
        dropdown.click()
        
        option = self.find_element(self.XPATH, toolbar_option_xpath)
        option.click()

        option = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((self.XPATH, toolbar_option_xpath))
        )

        if not option.is_selected():
            option.click()

        time.sleep(5)

    def get_proxies(self):
        soup = BeautifulSoup(self.page_source, 'html.parser')
        self.quit()
        proxy_elements = soup.find_all('tr', {'class': 'spy1xx'}) + soup.find_all('tr', {'class': 'spy1x'})
        for element in proxy_elements:
            try:
                proxy = element.find('td').getText()
                proxy_type = element.find_all('td')[1].find('a').find('font').getText()

                proxy_dict = {
                    'proxy': proxy,
                    'type': proxy_type.lower()
                }

                self.scraped_proxies.append(proxy_dict)
            except AttributeError:
                continue
