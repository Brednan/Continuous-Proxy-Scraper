from requests import Session
from bs4 import BeautifulSoup


class AdvancedName(Session):
    def __init__(self):
        Session.__init__(self)    
        self.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

        self.scraped_proxies = []
        self.TIMEOUT = 10

    def scrape_proxies(self):
        homepage = self.get('https://advanced.name/freeproxy', timeout=self.TIMEOUT)
        homepage_soup = BeautifulSoup(homepage.content, 'html.parser')
        page_list = homepage_soup.find('ul', {'class': 'pagination'}).find_all('li')
        page_list = [num.getText() for num in page_list[1: len(page_list) - 1]]

        for page_num in page_list:
            res = self.get(f'https://advanced.name/freeproxy?page={page_num}')
            soup = BeautifulSoup(res.content, 'html.parser')
            
            proxy_elements = soup.find('table', {'id': 'table_proxies'}).find('tbody').find_all('tr')
            for element in proxy_elements:
                print(element.getText())
