# encoding: utf-8

"""
Here we show how to retrieve RSS feeds from some popular (Dutch) newswebsites
"""

import feedparser  # Usefull to parse RSS feeds
from bs4 import BeautifulSoup as bs


class RssUrl:
    """
    RSS feeds for the news sites
    - NOS
    - NU
    - RTL

    Could add a lot more of course...
    """

    def __init__(self):
        """
        initializes the RssUrl.
        This allows you to easily create the urls to fetch data
        """
        self.url_dict = {'nos': {'label': ['nosnieuwsbinnenland', 'nossportalgemeen'],
                                 'name': ['nederland', 'sport'],
                                 'prefix': 'http://feeds.nos.nl/',
                                 'suffix': ''},
                         'nu': {'label': ['Algemeen', 'Sport'],
                                'name': ['algemeen', 'sport'],
                                'prefix': 'http://www.nu.nl/rss/',
                                'suffix': ''},
                         'rtl': {'label': ['nederland', 'Sport'],
                                 'name': ['nederland', 'sport'],
                                 'prefix': 'http://www.rtlnieuws.nl/service/rss/',
                                 'suffix': '/index.xml'}}
        self.news_source_list = self.url_dict.keys()

    def get_url_feed(self, news_source):
        """
        Returns the full url-feed you need for the given type

        Hence, you will get all the labels..
        """
        temp_dict = self.url_dict[news_source]
        url_feed = [temp_dict['prefix'] + x + temp_dict['suffix'] for x in temp_dict['label']]
        return url_feed

    def get_url_content(self, news_source):
        """
        Returns the content of the called RSS Feed

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent}

        :param news_source: nos, rtl or nu
        :return: Beautiful soup object that contains all the text that is being returned..
        """
        url_list = self.get_url_feed(news_source)  # This provides a list with URLs...
        label_name = self.url_dict[news_source]['name']  # This is the label name of the news category
        assert len(url_list) == len(label_name)  # These two should be of equal length

        news_text_list = []  # This list is used to store all the info of the news_source
        for i_name, i_url in zip(label_name, url_list):
            url_content = feedparser.parse(i_url)
            # Now we can loop over the individual news entries obtained from
            # the i_url link

            for i_entry in url_content['entries']:
                # Here we get all the entries and store these results in a temp dictionary
                # Could also been in done list comprehension.. but its not that more beautiful...
                temp_text = i_entry['summary_detail']['value']
                title_text = i_entry['title']
                content_text = bs(temp_text, 'lxml').text
                date_text = i_entry['published']
                temp_dict = {'title': title_text,
                             'content': content_text,
                             'date': date_text,
                             'category': i_name,
                             'source': news_source}
                news_text_list.append(temp_dict)

        return news_text_list

    def get_all_content(self):
        """
        Returns all the content we can find at this moment

        :return: list of text and labels
        """
        full_text = {}
        for i_news in self.news_source_list:
            full_text.update({i_news: self.get_url_content(i_news)})

        return full_text
