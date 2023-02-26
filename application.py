from Scrapers.geonode import GeonodeScraper, GeonodeException
from Scrapers.proxy_docker import ProxyDocker, ProxyDockerException
from Scrapers.spys_one import SpysOne, SpysException
from requests.exceptions import RequestException
from colorama import Fore
import time

class Application:
    def __init__(self):
        self.HTTP_PATH = './Scraped-Proxies/HTTP.txt'
        self.SOCKS4_PATH = './Scraped-Proxies/SOCKS4.txt'
        self.SOCKS5_PATH = './Scraped-Proxies/SOCKS5.txt'

        self.geonode = GeonodeScraper()
        self.proxy_docker = ProxyDocker()
        self.quit = False
        self.scrape_time = time.time()
        self.inc_scrape_time = 15 * 60

    def get_clock_time(self):
        float_time = time.time()
        time_structure = time.localtime(float_time)

        return time_structure

    def scrape_proxies(self):
        try:
            self.geonode.get_num_pages()

            if self.geonode.num_pages < 1:
                raise GeonodeException

            self.geonode.scrape_proxies()

        except RequestException as e:
            print(f"{Fore.RED}--- {self.get_clock_time_string()} Failed to scrape proxies from geonode! ---{Fore.RESET}\n")

        else:
            print(f'{Fore.GREEN}--- {self.get_clock_time_string()} Successfuly scraped proxies from geonode! ---{Fore.RESET}\n')

        try:
            self.proxy_docker.scrape_proxies()

        except (ProxyDockerException, RequestException):
            print(f"{Fore.RED}--- {self.get_clock_time_string()} Failed to scrape proxies from proxy docker! ---{Fore.RESET}\n")

        else:
            print(f'{Fore.GREEN}--- {self.get_clock_time_string()} Successfuly scraped proxies from proxy docker! ---{Fore.RESET}\n')

    def get_clock_time_string(self):
        display_time = self.get_clock_time()
        display_min = display_time.tm_min

        if display_min < 10:
            return f'Time: {display_time.tm_hour}:0{display_min} |'

        else:
            return f'Time: {display_time.tm_hour}:{display_min} |'

    def finished_scraping(self):
        self.scrape_time = time.time() + self.inc_scrape_time
        scrape_clock_time = time.localtime(self.scrape_time)
        
        print(f'{Fore.CYAN}--- {self.get_clock_time_string()} Finished scraping proxies! ---{Fore.RESET}\n')
        
        if scrape_clock_time.tm_min < 10:
            print(f'{Fore.CYAN}--- Next scrape will begin at {scrape_clock_time.tm_hour}:0{scrape_clock_time.tm_min} ---{Fore.RESET}\n')

        else:
            print(f'{Fore.CYAN}--- Next scrape will begin at {scrape_clock_time.tm_hour}:{scrape_clock_time.tm_min} ---{Fore.RESET}\n')
    
    def remove_duplicates(self, http: list, socks4: list, socks5: list):
        try:
            with open(self.HTTP_PATH, 'r') as f:
                http += f.read().strip().split('\n')

            with open(self.SOCKS4_PATH, 'r') as f:
                socks4 += f.read().strip().split('\n')

            with open(self.SOCKS5_PATH, 'r') as f:
                socks5 += f.read().strip().split('\n')

        except FileNotFoundError:
            pass

        http = list(dict.fromkeys(http))
        socks4 = list(dict.fromkeys(socks4))
        socks5 = list(dict.fromkeys(socks5))

        return (http, socks4, socks5)

    def export_proxies(self):
        scraped_proxies = self.geonode.scraped_proxies + self.proxy_docker.scraped_proxies
        
        http_scraped_proxies = [p['proxy'] for p in scraped_proxies if p['type'].lower() == 'http'] + [p['proxy'] for p in scraped_proxies if p['type'].lower() == 'https']
        socks4_scraped_proxies = [p['proxy'] for p in scraped_proxies if p['type'].lower() == 'socks4']
        socks5_scraped_proxies = [p['proxy'] for p in scraped_proxies if p['type'].lower() == 'socks5']

        duplicates_removed = self.remove_duplicates(http_scraped_proxies, socks4_scraped_proxies, socks5_scraped_proxies)

        http_no_duplicate = duplicates_removed[0]
        socks4_no_duplicate = duplicates_removed[1]
        socks5_no_duplicate = duplicates_removed[2]

        with open(self.HTTP_PATH, 'w') as f:
            for p in http_no_duplicate:
                if len(p) > 0:
                    f.write(f'{p}\n')
        
        with open(self.SOCKS4_PATH, 'w') as f:
            for p in socks4_no_duplicate:
                if len(p) > 0:
                    f.write(f'{p}\n')

        with open(self.SOCKS5_PATH, 'w') as f:
            for p in socks5_no_duplicate:
                if len(p) > 0:
                    f.write(f'{p}\n')

    def application(self):
        while not self.quit:
            if self.scrape_time - 1 < time.time() < self.scrape_time + 1:
                print(f'{Fore.CYAN}--- {self.get_clock_time_string()} Scraping proxies! ---{Fore.RESET}\n')

                self.scrape_proxies()
                self.export_proxies()
                self.finished_scraping()
