# -*- coding: utf-8 -*-

from abstract_crawler import AbstractCrawler
from wired_collector.scraper import WiredScraper


class WiredCrawler(AbstractCrawler):

    def __init__(self, target_url, save_dir="./data", page_count=1):
        super(WiredCrawler, self).__init__(
            WiredScraper, target_url, save_dir, page_count
        )

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)
        div_pagination = soup.find("div", {"class": "pagination"})
        a_next = div_pagination.find("a", {"class": "next"})

        if a_next is not None and "href" in a_next.attrs:
            next_page_url = a_next["href"]

            if self.before_url != next_page_url:
                print("[ PROCESS ] Next article list page: {}".format(url))
                return next_page_url

        return None
