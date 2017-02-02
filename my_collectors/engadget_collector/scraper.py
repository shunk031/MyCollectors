# -*- coding: utf-8 -*-

from abstract_scraper import AbstractScraper
from urllib.parse import urljoin
import traceback


class EngadgetScraper(AbstractScraper):

    base_url = "https://engadget.com/"
    none_count = 0

    def __init__(self, target_url, save_dir):
        super(EngadgetScraper, self).__init__(
            target_url, save_dir
        )

    def get_article_detail_urls(self):

        soup = self._make_soup(self.target_url)

        # 記事概要のそれぞれのデータを取得する
        div_grid_tl = soup.find("div", {"class": "grid@tl+"})
        div_containers = div_grid_tl.find_all("div", {"class": "container@m"})

        # 記事詳細へのURLを取得する
        article_detail_url_list = []
        for i, div_container in enumerate(div_containers):

            if i == 0:
                detail_url = div_container.find("h2").find("a")
            else:
                detail_url = div_container.find("a", {"class": "o-hit__link"})

            try:
                abs_url = detail_url["href"]
                url = urljoin(self.base_url, abs_url)
                print("[ GET ] Get URL: {}".format(url))
                article_detail_url_list.append(url)
            except TypeError as err:
                traceback.print_tb(err.__traceback__)
                pass

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):

        article_dict = {}
        article_dict["url"] = article_url

        detail_soup = self._make_soup(article_url)
        title_tag = detail_soup.find("h1", {"class": "t-h4@m-"})
        try:
            title = title_tag.get_text().strip()
        except AttributeError as err:
            traceback.print_tb(err.__traceback__)
            title = str(self.none_count)
            self.none_count += 1

        print("[ GET ] Title: {}".format(title))
        article_dict["title"] = title

        try:
            div_article_texts = detail_soup.find_all("div", {"class": "artcile-text"})
            article_content = [div_article_text.get_text().strip() for div_article_text in div_article_texts]
            article_content = " ".join(article_content)
        except AttributeError as err:
            traceback.print_tb(err.__traceback__)
            article_content = None

        article_dict["article"] = article_content

        return article_dict
