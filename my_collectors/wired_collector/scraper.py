# -*- coding: utf-8 -*-

from my_collectors.abstract_scraper import AbstractScraper
import traceback


class WiredScraper(AbstractScraper):

    def __init__(self, target_url, save_dir):
        super(WiredScraper, self).__init__(
            target_url, save_dir
        )

    def get_article_detail_urls(self):
        soup = self._make_soup(self.target_url)

        # 記事概要一覧を取得する
        ul_col = soup.find("ul", {"class": "col"})

        # 記事概要のそれぞれのデータを取得する
        li_articles = ul_col.find_all("li")

        # 記事詳細へのURLを取得する
        article_detail_url_list = []
        for li_article in li_articles:
            a_pad = li_article.find("a", {"class": "clearfix"})
            url = a_pad["href"]
            print("[ GET ] Get URL: {}".format(url))
            article_detail_url_list.append(url)

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):

        article_dict = {}
        article_dict["url"] = article_url

        detail_soup = self._make_soup(article_url)
        h1_post_title = detail_soup.find("h1", {"class": "post-title"})
        title = h1_post_title.get_text().strip()

        print("[ GET ] Title: {}".format(title))
        article_dict["title"] = title

        article_content = detail_soup.find("article", {"class": "content"})
        article_content = article_content.get_text()

        article_dict["article"] = article_content.strip()

        ul_article_tag = detail_soup.find("ul", {"id": "article-tags"})
        article_tags = ul_article_tag.find_all("a")
        article_tag_list = []
        for article_tag in article_tags:
            # print(article_tag.get_text())
            article_tag_list.append(article_tag.get_text())

        article_dict["topics"] = article_tag_list

        return article_dict
