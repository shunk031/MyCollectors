# -*- coding: utf-8 -*-

from my_collectors.abstract_crawler import AbstractCrawler
from my_collectors.engadget_collector.scraper import EngadgetScraper
from urllib.parse import urljoin


class EngadgetCrawler(AbstractCrawler):

    base_url = "https://engadget.com/"

    def __init__(self, target_url, save_dir="./engadget_data", page_count=1):
        super(EngadgetCrawler, self).__init__(
            EngadgetScraper, target_url, save_dir, page_count
        )

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)
        a_next = soup.find("a", {"class": "o-btn--small"})

        if a_next is not None and "href" in a_next.attrs:
            abs_next_page_url = a_next["href"]
            next_page_url = urljoin(self.base_url, abs_next_page_url)

            if self.before_url != next_page_url:
                print("[ PROCESS ] Next article list page: {}".format(url))
                return next_page_url

        return None
