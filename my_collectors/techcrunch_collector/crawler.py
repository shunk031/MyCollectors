# -*- coding: utf-8 -*-

from abstract_crawler import AbstractCrawler
from techcrunch_collector.scraper import TechcrunchScraper

from urllib.parse import urljoin


class TechcrunchCrawler(AbstractCrawler):

    base_url = "https://techcrunch.com/"

    def __init__(self, target_url, save_dir="./data", page_count=1):
        super(TechcrunchCrawler, self).__init__(
            TechcrunchScraper, target_url, save_dir, page_count
        )

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)

        ol_pagination = soup.find("ol", {"class": "pagination"})
        a_next = ol_pagination.find("li", {"class": "next"}).find("a")

        # print("a_next: {}".format(a_next["href"]))

        if a_next is not None and "href" in a_next.attrs:
            abs_next_page_url = a_next["href"]
            next_page_url = urljoin(self.base_url, abs_next_page_url)

            if self.before_url != next_page_url:
                print("[ PROCESS ] Next article list page: {}".format(url))
                return next_page_url

        return None
