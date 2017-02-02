# -*- coding: utf-8 -*-

from abstract_scraper import AbstractScraper
import traceback


class TechcrunchScraper(AbstractScraper):

    base_url = "https://techcrunch.com/page/1/"

    def __init__(self, target_url, save_dir):
        super(TechcrunchScraper, self).__init__(
            target_url, save_dir
        )

    def get_article_detail_urls(self):

        soup = self._make_soup(self.target_url)

        # 記事概要のそれぞれのデータを取得する
        div_l_main_containers = soup.find_all("div", {"class": "l-main-container"})
        li_river_blocks_list = []
        for div_l_main_container in div_l_main_containers:
            li_river_blocks = div_l_main_container.find_all("li", {"class": "river-block"})

            for li_river_block in li_river_blocks:
                li_river_blocks_list.append(li_river_block)

        article_detail_url_list = []
        for li_river_block in li_river_blocks_list:
            if "data-permalink" in li_river_block.attrs:
                url = li_river_block["data-permalink"]
            else:
                url = li_river_block.find("a")
                url = url["href"]
            print("[ GET ] Get URL: {}".format(url))

            article_detail_url_list.append(url)

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):

        article_dict = {}
        article_dict["url"] = article_url

        detail_soup = self._make_soup(article_url)

        try:
            h1_tweet_title = detail_soup.find("h1", {"class": "tweet-title"})

        except AttributeError as err:
            traceback.print_tb(err.__traceback__)
            h1_tweet_title = detail_soup.find("h1")

        title = h1_tweet_title.get_text().strip()
        print("[ GET ] Title: {}".format(title))

        article_dict["title"] = title

        try:
            div_article_entry = detail_soup.find("div", {"class": "article-entry"})
            p_article_texts = div_article_entry.find_all("p")
            article_content = [p_article_text.get_text() for p_article_text in p_article_texts]
            article_content = " ".join(article_content)

        except AttributeError as err:
            traceback.print_tb(err.__traceback__)
            article_content = None

        article_dict["article"] = article_content

        return article_dict
