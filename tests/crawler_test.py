# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
import random
import time
sys.path.append(os.pardir)

from my_collectors.engadget_collector.crawler import EngadgetCrawler
from my_collectors.research_blogging_collector.crawler import ResearchBloggingCrawler
from my_collectors.techcrunch_collector.crawler import TechcrunchCrawler
from my_collectors.wired_collector.crawler import WiredCrawler

from slacker import Slacker
from urllib.error import HTTPError

HOME_DIR = os.path.expanduser("~")

crawlers = {
    "engadget": EngadgetCrawler,
    "researchblogging": ResearchBloggingCrawler,
    "techcrunch": TechcrunchCrawler,
    "wired": WiredCrawler,
}

target_urls = {
    "engadget": "https://www.engadget.com/topics/science/page/1",
    "researchblogging": "http://www.researchblogging.org/",
    "techcrunch": "https://techcrunch.com/page/1",
    "wired": "https://www.wired.com/category/science/page/1",
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Test crawler work")
    parser.add_argument("--crawler", "-c", choices=crawlers.keys())
    args = parser.parse_args()

    status_file = args.crawler + "-status.json"
    if os.path.isfile(status_file):
        with open(status_file, "r") as rf:
            status_dict = json.load(rf)

        target_url = status_dict["target_url"]
        page_count = status_dict["page_count"]
    else:
        target_url = target_urls[args.crawler]
        page_count = 1

    crawler = crawlers[args.crawler](target_url, "./dump_files", page_count=page_count)

    slacker_config_path = os.path.join(HOME_DIR, ".slacker.config")
    with open(slacker_config_path, "r") as rf:
        slacker_config = json.load(rf)

    slacker = Slacker(slacker_config["token"])

    start_id = random.randint(0, 1000)
    finish_crawl = crawler.crawl()

    max_retries = 3
    retries = 0
    while True:
        try:
            slacker.chat.post_message("#crawler", "{}: {}, {}".format(crawler.__class__.__name__, start_id, finish_crawl))
        except HTTPError as http_err:
            retries += 1
            if retries >= max_retries:
                raise Exception("Too many retries.")

            wait = 2 ** (retries - 1)
            print("[ RETRY ] Waiting {} seconds...".format(wait))
            time.sleep(wait)
