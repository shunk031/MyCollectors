# -*- coding: utf-8 -*-

from my_collectors.abstract_crawler import AbstractCrawler
from my_collectors.research_blogging_collector.scraper import ResearchBloggingScraper


class ResearchBloggingCrawler(AbstractCrawler):

    def __init__(self, target_url, save_dir="./data", page_count=1):
        super(ResearchBloggingCrawler, self).__init__(
            ResearchBloggingScraper, target_url, save_dir, page_count
        )

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)
        ul_pageBrowser = soup.find("ul", {"class": "pageBrowser"})
        try:
            a_nexts = ul_pageBrowser.find_all("a", {"class": "underlined"})
            a_next = a_nexts[1]
        except:
            a_next = ul_pageBrowser.find("a", {"class": "underlined"})

        if a_next is not None and "href" in a_next.attrs:
            next_page_url = a_next["href"]

            if self.before_url != next_page_url:
                print("[ PROCESS ] Next article list page: {}".format(url))
                return next_page_url

        return None
