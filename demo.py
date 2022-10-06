from src.constants import *
#from src.data_collection.data_collection import NytAPI
#from src.data_collection.indian_news_collection import NewsCollection
from src.db.mongodb import DBOps
from src.data_processing.text_processing import TextProcessing
from src.inference.preds import Inference
from src.utils.util import read_yaml
from src.exception import CustomException
from src.logger import logging
from datetime import datetime

sample_news = '''Congress MP Shashi Tharoor, who has thrown his hat in the ring for the party president post, said that leaders like Mallikarjun Kharge can’t bring changes to the party and will continue the existing system.'''

class Demo:
    def __init__(self, text, headline=None, keyword=None):
        self.text = text
        self.headline = headline
        self.keyword = keyword
        self.date = f"{datetime.now().strftime('%Y-%m-%d')}"
    
    def run(self):
        data = {'date': self.date, 'keyword': self.keyword, 'headline': self.headline, 'text': self.text, 'summary': None}
        """dbops = DBOps()
        insertionCheckQuery = {"keyword": self.keyword, "date": self.date}
        records = dbops.findFirstRecord('news_summary', 'news_db', query=insertionCheckQuery)
        if records is None:
            dbops.insertRecord('news_summary', 'news_db', data)
        #dbops.dbCloseConnection(dbops.dbMongoClient())"""
        text = TextProcessing(self.text).text_cleaning()
        summary = Inference().inference(text)
        print(summary)

if __name__ == '__main__':
    a = Demo(sample_news, keyword='trump')
    print(a.run())