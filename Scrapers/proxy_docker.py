from requests import Session
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time
from colorama import Fore


class ProxyDockerException(Exception):
    pass

class ProxyDockerHTTPException(Exception):
    pass

class ProxyDockerSOCKS4Exception(Exception):
    pass

class ProxyDockerSOCKS5Exception(Exception):
    pass

class ProxyDocker(Session):
    def __init__(self):
        Session.__init__(self)

        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        })

        self.url = 'https://www.proxydocker.com/en/'
        self.post_url = 'https://www.proxydocker.com/en/api/proxylist/'
        self.scraped_proxies = []
        self.token = None

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

    def get_token(self):
        res = self.get(self.url).content
        soup = BeautifulSoup(res, 'html.parser')
        
        self.token = soup.find('meta', {'name':'_token'})['content']

    def get_http_proxies(self):
        try:
            page_num = 1

            proxies = []

            while page_num <= 3:
                http_payload = {
                    'token': self.token,
                    'country': 'all',
                    'city': 'all',
                    'state': 'all',
                    'port': 'all',
                    'type': 'http-https',
                    'anonymity': 'all',
                    'need': 'all',
                    'page': page_num
                }

                page = self.post(self.post_url, data=http_payload).json()
                proxies += page['proxies']
                page_num += 1

            for proxy in proxies:
                proxy_dict = {
                    'proxy': f'{proxy["ip"]}:{proxy["port"]}',
                    'type': 'http'
                }

                self.scraped_proxies.append(proxy_dict)
        
        except RequestException:
            print(f"{Fore.YELLOW}--- {self.get_clock_time_string()} Failed to scrape HTTP proxies from page {page} on proxy docker! ---{Fore.RESET}\n")

    def get_socks4_proxies(self):
        try:
            proxies = []
            
            page_num = 1
            while page_num <= 3:
                socks4_payload = {
                    'token': self.token,
                    'country': 'all',
                    'city': 'all',
                    'state': 'all',
                    'port': 'all',
                    'type': 'socks4',
                    'anonymity': 'all',
                    'need': 'all',
                    'page': page_num
                    }

                page = self.post(self.post_url, data=socks4_payload).json()
                proxies += page['proxies']
                page_num += 1

            for proxy in proxies:
                proxy_dict = {
                    'proxy': f'{proxy["ip"]}:{proxy["port"]}',
                    'type': 'socks4'
                }

                self.scraped_proxies.append(proxy_dict)

        except RequestException:
            print(f"{Fore.YELLOW}--- {self.get_clock_time_string()} Failed to scrape SOCKS4 proxies from page {page} on proxy docker! ---{Fore.RESET}\n")

    def get_socks5_proxies(self):
        try:
            proxies = []

            page_num = 1
            while page_num <= 3:
                socks5_payload = {
                    'token': self.token,
                    'country': 'all',
                    'city': 'all',
                    'state': 'all',
                    'port': 'all',
                    'type': 'socks4',
                    'anonymity': 'all',
                    'need': 'all',
                    'page': page_num
                    }

                page = self.post(self.post_url, data=socks5_payload).json()
                proxies += page['proxies']
                page_num += 1
            
            for proxy in proxies:
                proxy_dict = {
                    'proxy': f'{proxy["ip"]}:{proxy["port"]}',
                    'type': 'socks5'
                }

                self.scraped_proxies.append(proxy_dict)

        except RequestException:
            print(f"{Fore.YELLOW}--- {self.get_clock_time_string()} Failed to scrape SOCKS5 proxies from page {page} on proxy docker! ---{Fore.RESET}\n")

    def scrape_proxies(self):
        try:
            self.get_token()

        except:
            raise ProxyDockerException

        if not self.token:
            raise ProxyDockerException

        self.get_http_proxies()
        self.get_socks4_proxies()
        self.get_socks5_proxies()