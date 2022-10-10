import requests
from bs4 import BeautifulSoup
from src.exception import CustomException
import sys
import re

class VoxNewsArticle:
    def __init__(self, keyword, cdate):
        self.keyword = keyword.lower()
        self.date = cdate

    def text_article(self):
        try:
            url = url = f'https://www.vox.com/search?order=date&q={self.keyword}'
            page = requests.get(url)
            bs = BeautifulSoup(page.content, 'html.parser')
            article_page = bs.findAll('a', attrs={'data-analytics-link':'article'})
            if len(article_page) == 0:
                return 'No Article found', 'No Article found', self.date
            article_page = article_page[0]['href']
            article_page = requests.get(article_page)
            bs = BeautifulSoup(article_page.content, 'html.parser')
            headline = bs.find('h1', attrs={'class': 'c-page-title'}).text
            date = re.sub(r'\n', '', bs.find('time', attrs={'data-ui': 'timestamp'}).text).strip()
            text = ' '.join(item.text for item in bs.find('div', attrs={'class': 'c-entry-content'}).findAll('p', attrs={}, recursive=False))
            return headline, text, date
        except CustomException as e:
            raise CustomException(e, sys) from e
