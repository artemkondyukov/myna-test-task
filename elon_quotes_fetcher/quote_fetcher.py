from bs4 import BeautifulSoup
import requests
from typing import Iterable


class QuoteFetcher:
    @staticmethod
    def fetch_quote(url: str) -> Iterable[str]:
        """
        Takes url from https://elonmusknews.org, downloads the page
        Do the parsing, finding quotes on the page and returns them
        :param url: link to the page in form 'https://elonmusknews.org/blog/<PAGE>'
        :return: yields texts
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")
        content_div = soup.find_all("div", attrs={"class": "sqs-block-content"})[0]

        if len(content_div) == 0:
            raise ValueError("Wrong page structure, no div of class sqs-block-content")

        for li in content_div.find_all("li"):
            yield li.text
