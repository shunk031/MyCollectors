# -*- coding: utf-8 -*-

import time
import json

from abc import ABCMeta, abstractmethod
from my_collectors.base_collector import BaseCollector


class AbstractCrawler(BaseCollector, metaclass=ABCMeta):

    FINISH_CRAWL = "Finish crawl."

    def __init__(self, scraper_class, target_url, save_dir="./data", page_count=1):

        self.target_url = target_url
        self.before_url = None
        self.save_dir = save_dir
        self.page_count = page_count

        self.scraper_class = scraper_class

    @abstractmethod
    def get_next_page_link(self, url):
        pass

    def crawl(self):
        try:
            while True:
                # start to measure the time
                start = time.time()
                print("[ PROCESS ] Now page {} PROCESSING".format(self.page_count))
                scraper = self.scraper_class(self.target_url, self.save_dir)
                scraper.scrap()  # scraping!
                # get next page link url
                self.target_url = self.get_next_page_link(self.target_url)

                # if target_url is not found
                if self.target_url is None:
                    break

                self.page_count += 1
                time.sleep(2)
                end = time.time()  # end to measure the time

                # print processing time
                self._print_processing_time(start, end)

        except KeyboardInterrupt as err:
            print("[ EXCEPTION ] Exception occured: {}".format(err))

            # save crawler status
            self.save_crawler_status()

        return self.FINISH_CRAWL

    def _print_processing_time(self, start_time, end_time):

        elapsed_sec = end_time - start_time
        elapsed_min = elapsed_sec / 60

        if elapsed_min < 1:
            print("[ TIME ] Elapsed time: {:.2f} [sec]".format(elapsed_sec))
        else:
            print("[ TIME ] Elapsed time: {:.2f} [min]".format(elapsed_min))

    def save_crawler_status(self):

        status_dict = {}
        status_dict["target_url"] = self.target_url
        status_dict["page_count"] = self.page_count

        status_filename = self.scraper_class.__name__ + "-status.json"

        with open(status_filename, "w") as wf:
            json.dump(status_dict, wf, indent=2)

        print("[ SAVE ] Save status.json")
