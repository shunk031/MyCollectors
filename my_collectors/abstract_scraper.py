# -*- coding: utf-8 -*-

import os
import csv
import traceback
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead

from abc import ABCMeta, abstractmethod
from my_collectors.base_collector import BaseCollector


class AbstractScraper(BaseCollector, metaclass=ABCMeta):

    def __init__(self, target_url, save_dir):
        self.target_url = target_url
        self.save_dir = save_dir

    def scrap(self):
        # get list of detail article url
        article_detail_url_list = self.get_article_detail_urls()

        article_detail_info = []
        for article_url in article_detail_url_list:
            try:
                article_dict = self.get_article_detail_info_dict(article_url)
                article_detail_info.append(article_dict)
            except (AttributeError, HTTPError, UnicodeEncodeError, UnicodeError,
                    URLError, IncompleteRead, ConnectionResetError, LookupError) as err:
                print("[ EXCEPTION ] Exception occured in scrap(): {}".format(err))
                # traceback.print_tb(err.__traceback__)

        self.save_article_detail_info_list_to_csv(article_detail_info)

    @abstractmethod
    def get_article_detail_urls(self):
        pass

    @abstractmethod
    def get_article_detail_info_dict(self, article_url):
        pass

    def create_article_dict(self, title, url, article):

        article_dict = {}
        article_dict["title"] = title
        article_dict["url"] = url
        article_dict["article"] = article

        return article_dict

    def save_article_detail_info_list_to_csv(self, article_detail_info_list):

        # if not exist save_dir, make the directory
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        for article_detail_dict in article_detail_info_list:
            article_title = article_detail_dict["title"]
            csv_filename = self._convert_filename(article_title)
            csv_filename = "{}.csv".format(csv_filename)

            if "topics" in article_detail_dict.keys():
                output_info = [article_detail_dict["title"],
                               article_detail_dict["url"],
                               article_detail_dict["article"],
                               article_detail_dict["topics"]]
            else:
                output_info = [article_detail_dict["title"],
                               article_detail_dict["url"],
                               article_detail_dict["article"]]

            with open(os.path.join(self.save_dir, csv_filename), "w") as wf:
                writer = csv.writer(wf)
                writer.writerow(output_info)

    def _convert_filename(self, article_title):

        filename = article_title.replace(" ", "_")
        filename = filename.replace("/", "")
        filename = filename.replace("?", "")

        if len(filename) > 250:
            filename = filename[:250]
        return filename
