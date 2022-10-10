import pandas as pd
import sys
import pymongo
from src.logger import logging
from src.exception import CustomException
from src.constants import *
from src.utils.util import read_yaml


class DBOps:
    def __init__(self):
        self.username = read_yaml(SECRET_PATH)[DB][USERNAME]
        self.password = read_yaml(SECRET_PATH)[DB][PASSWORD]
        self.url = f'mongodb+srv://{self.username}:{self.password}@cluster0.zyiqjp2.mongodb.net/?retryWrites=true&w=majority'

    """
    def __mongoDbClient(self):
        #This function creates a client for connection purpose
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            raise CustomException(e, sys) from e

    def closeMongoDbConnection(self, client):
        #Function closes the active mongo db connection
        try:
            client.close()
        except Exception as e:
            raise CustomException(e, sys) from e
    """

    def isDBPresent(self, db_name):
        """
        Function returns true or false if the db is available
        """
        try:
            client = pymongo.MongoClient(self.url)
            print(client)
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise CustomException(e, sys) from e

if __name__ == '__main__':
    a = DBOps()
    #insertionCheckQuery = {"keyword": "modi", "date": "2022-10-01"}
    records = a.isDBPresent('news_db')
    print(records)