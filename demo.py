import sys
from src.constants import *
#from src.data_collection.data_collection import NytAPI
#from src.data_collection.indian_news_collection import NewsCollection
from src.data_collection.vox_news_collection import VoxNewsArticle
#from src.db.mongodb import DBOps
#from src.db.cassandradb import DBOps
from src.data_processing.text_processing import TextProcessing
from src.inference.preds import Inference
from src.utils.util import read_yaml
from src.exception import CustomException
from src.logger import logging
from datetime import datetime

class Demo:
    def __init__(self, keyword):
        self.keyword = keyword
        self.date = f"{datetime.now().strftime('%Y-%m-%d')}"
    
    def run(self):
        try:
            data = {'date': self.date, 'keyword': self.keyword, 'headline': None, 'text': None, 'summary': None}
            headline, text, date = VoxNewsArticle(keyword=self.keyword, cdate=self.date).text_article()
            if headline != 'No Article found':
                text = TextProcessing(text=text).text_cleaning()
                summary = Inference().inference(text=text)
                data.update({
                    'date': date,
                    'headline': headline,
                    'text': text,
                    'summary': summary
                })
            else:
                data.update({
                    'headline': headline,
                    'text': text,
                })
            #db = DBOps()
            #db.insertOneRecord(table_name='news', values=[data['date'], data['headline'], data['keyword'], data['summary']])
            #return data
            return data['headline'], data['summary'], data['date'], data['keyword']
        
        except Exception as e:
            raise CustomException(e, sys) from e
        

if __name__ == '__main__':
    a = Demo(keyword='trump')
    print(a.run())