from requests import Session
from requests.exceptions import RequestException
import time
from colorama import Fore


class GeonodeException(Exception):
    pass


class GeonodeScraper(Session):
    def __init__(self):
        Session.__init__(self)
        self.setHeaders()
        self.num_pages = 0
        self.scraped_proxies = []

    def get_clock_time(self):
        float_time = time.time()
        time_structure = time.localtime(float_time)

        return time_structure

    def get_clock_time_string(self):
        display_time = self.get_clock_time()
        display_min = display_time.tm_min

        if display_min < 10:
            return f'Time: {display_time.tm_hour}:0{display_min} |'

        else:
            return f'Time: {display_time.tm_hour}:{display_min} |'

    def scrape_proxies(self):
        page_num = 1
        
        while page_num <= self.num_pages:
            try:
                url = f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={page_num}&sort_by=lastChecked&sort_type=desc'
                res = self.get(url, timeout=10).json()
                proxies = res['data']

                for proxy in proxies:

                    proxy_dict = {
                        'proxy': f'{proxy["ip"]}:{proxy["port"]}',
                        'type': proxy['protocols'][0]
                    }

                    self.scraped_proxies.append(proxy_dict)
                
            except RequestException:
                print(f"{Fore.YELLOW}--- {self.get_clock_time_string()} Failed to scrape proxies from page {page_num} on geonode! ---{Fore.RESET}\n")

            page_num += 1

    def get_num_pages(self):
        url = 'https://proxylist.geonode.com/api/proxy-list'

        res = self.get(url, timeout=10).json()

        total_num_proxies = res['total']
        self.num_pages = int(total_num_proxies/500) + 1

    def setHeaders(self):
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        })