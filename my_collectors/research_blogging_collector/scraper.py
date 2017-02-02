# -*- coding: utf-8 -*-

from abstract_scraper import AbstractScraper
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from http.client import IncompleteRead
from bs4 import BeautifulSoup
from readability.readability import Document
import traceback


class ResearchBloggingScraper(AbstractScraper):

    base_url = "http://www.researchblogging.org/"
    user_agent = "Mozilla/5.0 (Windows U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    headers = {"User-Agent": user_agent, }

    def __init__(self, target_url, save_dir):
        super(ResearchBloggingScraper, self).__init__(
            target_url, save_dir
        )

    def get_article_detail_urls(self):

        soup = self._make_soup(self.target_url)

        # 記事概要のそれぞれのデータを取得する
        div_leftCol = soup.find("div", {"id": "leftCol"})

        div_mainArticles = div_leftCol.find_all("div", {"class": "mainArticle"})
        div_mainArticleBottom = div_leftCol.find("div", {"id": "mainArticleBottom"})

        div_main_article_list = [div_mainArticle for div_mainArticle in div_mainArticles]

        div_main_article_list.append(div_mainArticleBottom)

        article_detail_url_list = []
        for div_main_article in div_main_article_list:
            detail_url = div_main_article.find("h1").find("a")
            abs_url = detail_url["href"]
            url = urljoin(self.base_url, abs_url)
            print("[ GET ] Get URL: {}".format(url))

            # ページ構成の都合上、ここでタイトルを取得する。
            title = detail_url.get_text().strip()

            # [(url1, title1), (url2, title2), ]の形でリストに追加していく
            article_detail_url_list.append((url, title))

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):

        article_dict = {}
        title = article_url[1].strip()

        url = article_url[0]
        article_dict["url"] = url

        print("[ GET ] Title: {}".format(title))
        article_dict["title"] = title

        try:
            request = Request(url, None, self.headers)

            with urlopen(request) as res:
                attempt = 0
                while attempt < 3:
                    try:
                        html = res.read()
                    except IncompleteRead as e:
                        attempt += 1
                    else:
                        break

            readable_article = Document(html).summary()
            readable_soup = BeautifulSoup(readable_article, "lxml")
            article_dict["article"] = readable_soup.get_text()

        except Exception as err:
            traceback.print_tb(err.__traceback__)
            article_dict["article"] = None

        return article_dict
