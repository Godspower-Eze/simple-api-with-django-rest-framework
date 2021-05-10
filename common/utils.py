from bs4 import BeautifulSoup
import requests
import logging

from pathlib import Path

home = Path.home()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(home / 'contract.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Scrapper:

    def __init__(self):
        self.theblockcrypto_url = "https://www.theblockcrypto.com/"

    def scrapper_for_theblockcrypto(self):
        """

        A method that scraps https://www.theblockcrypto.com/ to get the latest articles

        """
        request = requests.get(self.theblockcrypto_url)

        soup = BeautifulSoup(request.content, 'lxml')

        try:
            storyFeed_div = soup.find('div', class_="storyFeed")

            article = storyFeed_div.findAll('article')

            response_list = list()

            for i in article:
                data = {}
                url = "https://www.theblockcrypto.com"
                label = i.label.text
                data['label'] = label
                title = i.a.h3.text
                data['title'] = title
                link = f"{url}{i.a['href']}"
                data['link'] = link
                description = i.find("div", class_="font-body").div
                if description is not None:
                    data['description'] = description.text
                else:
                    data['description'] = None
                response_list.append(data)
            return response_list
        except Exception:
            logger.exception("An error occured while trying fetch scrap the site theblockcrypto.com")
            return False


class PriceGetter:

    def __init__(self):
        self.endpoint = "https://api.coingecko.com/api/v3/simple/price"

    def get_price(self, id, denomination):
        request = requests.get(f"{self.endpoint}?ids={id}&vs_currencies={denomination}")
        return request.content
