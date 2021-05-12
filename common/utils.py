import os
from bs4 import BeautifulSoup
import requests
import logging
from web3 import Web3
import json
from pathlib import Path

home = Path.home()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(home / 'contract.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

ETHERSCAN_KEY = os.environ.get('ETHERSCAN_KEY')


def convert_wei_to_ether(value):
    value = value / 1000000000000000000
    return value


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
        """
        A method thats the price of a token from coingecko
        """

        request = requests.get(f"{self.endpoint}?ids={id}&vs_currencies={denomination}")
        return request.content

    def get_amount_of_token_in_an_address(self, address="0xb2ecd701b01fd80d38fdf88021035d22c9a370e2"):

        """
        A method that gets the amount of ether in an address
        """
        address_checker = Web3.isAddress(address)
        if address_checker:
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_KEY}"
            request = requests.get(url)
            response = json.loads(request.content)
            value_in_wei = int(response['result'])
            value_in_ether = convert_wei_to_ether(value_in_wei)
            return value_in_ether
        else:
            logger.debug("The address you passed in is not valid")
            return False
