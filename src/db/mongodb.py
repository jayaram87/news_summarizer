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
        #self.url = f'mongodb+srv://{self.username}:{self.password}@cluster0.zyiqjp2.mongodb.net/test'

    def dbMongoClient(self):
        """
        Function creates mongo db client object for connection
        """
        try:
            client = pymongo.MongoClient(self.url)
            print(client)
            return client
        except Exception as e:
            raise CustomException(e, sys) from e

    def dbCloseConnection(self, db_client):
        """
        Function closes the db client connection
        """
        try:
            db_client.close()
        except Exception as e:
            raise CustomException(e, sys) from e

    def isDBPresent(self, db_name):
        """
        Function checks whether the db is available or not
        """
        try:
            client = self.dbMongoClient()
            if db_name in client.list_database_names():
                self.dbCloseConnection(client)
                return True
            else:
                self.dbCloseConnection(client)
                return False
        except Exception as e:
            raise CustomException(e, sys) from e

    def createDB(self, db_name):
        """
        Function creates a new database
        """
        try:
            db_available = self.isDBPresent(db_name)
            if db_available:
                client = self.dbMongoClient()
                db = client[db_name]
                self.dbCloseConnection(client)
                return db
            else:
                client = self.dbMongoClient()
                db = client[db_name]
                self.dbCloseConnection(client)
                return db
        except Exception as e:
            raise CustomException(e, sys) from e

    def dropDB(self, db_name):
        """
        Function deletes the database
        """
        try:
            db_available = self.isDBPresent(db_name)
            client = self.dbMongoClient()
            if db_available:
                client.drop_database(db_name)
                self.dbCloseConnection(client)
                return True
            else:
                logging.info(f'{db_name} is not available')
        except Exception as e:
            raise CustomException(e, sys) from e

    def getDb(self, db_name):
        """
        Function return the db
        """
        try:
            db = self.createDB(db_name)
            return db
        except Exception as e:
            raise CustomException(e, sys) from e

    def isCollectionPresent(self, collection_name, db_name):
        """
        Function checks whether the collection is available in the db
        """
        try:
            db_available = self.isDBPresent(db_name)
            if db_available:
                db = self.getDb(db_name)
                if collection_name in db.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise CustomException(e, sys) from e

    def createCollection(self, collection_name, db_name):
        """
        Function creates a collection in db_name
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if not collection_available:
                db = self.getDb(db_name)
                collection = db[collection_name]
                return collection
        except Exception as e:
            raise CustomException(e, sys) from e

    def dropCollection(self, collection_name, db_name):
        """
        Function deletes the collection from the db
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def getCollection(self, collection_name, db_name):
        """
        Function returns the collection in the db
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                db = self.getDb(db_name)
                return self.MongoClient()[db[collection_name]]
            else:
                collection = self.createCollection(collection_name, db_name)
                return collection
        except Exception as e:
            raise CustomException(e, sys) from e

    def insertRecord(self, collection_name, db_name, record):
        """
        Function inserts the record into the collection
        record keys: date, time, text, headline, summary
        """
        try:
            collection = self.getCollection(collection_name, db_name)
            collection.insert_one(record)
            self.dbCloseConnection()
            return f'Record has been inserted'
        except Exception as e:
            raise CustomException(e, sys) from e

    def insertRecords(self, collection_name, db_name):
        """
        Function inserts multiple records into the collection
        """
        try:
            collection = self.getCollection(collection_name, db_name)
            record = list(record.values())
            collection.insert_many(record)
            return f'Records inserted'
        except Exception as e:
            raise CustomException(e, sys) from e

    def findFirstRecord(self, collection_name, db_name, query=None):
        """
        Function returns the collection records based on the query
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                first_record = collection.find_one(query)
                self.dbCloseConnection()
                return first_record
        except Exception as e:
            raise CustomException(e, sys) from e

    def findRecords(self, collection_name, db_name, query=None):
        """
        Function returns multiple records based on the query
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                records = collection.find({},query)
                self.dbCloseConnection()
                return records
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def updateARecord(self, collection_name, db_name, query=None):
        """
        Function updates one record based on the query
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                records = collection.find()
                update_record = collection.update(records, query)
                return update_record
        except Exception as e:
            raise CustomException(e, sys) from e

    def updateRecords(self, collection_name, db_name, query=None):
        """
        Function updates multiple records
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                records = collection.find()
                update_records = collection.updata_many(records, query)
                return update_records
        except Exception as e:
            raise CustomException(e, sys) from e

    def deleteRecord(self, collection_name, db_name, query=None):
        """
        Function deletes a record
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                collection.delete_one(query)
                return f'Record deleted'
        except Exception as e:
            raise CustomException(e, sys) from e

    def deleteRecords(self, collection_name, db_name, query=None):
        """
        Function deletes multiple records
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                collection.delete_many(query)
                return f'Records deleted'
        except Exception as e:
            raise CustomException(e, sys) from e

    def getDataFrame(self, collection_name, db_name, query=None):
        """
        Function returns a pandas df for display
        """
        try:
            collection_available = self.isCollectionPresent(collection_name, db_name)
            if collection_available:
                collection = self.getCollection(collection_name, db_name)
                df = pd.DataFrame(collection.find(query))
                return df
        except Exception as e:
            raise CustomException(e, sys) from e
"""
a = DBOps()
insertionCheckQuery = {"keyword": "modi", "date": "2022-10-01"}
records = a.findFirstRecord('news_summary', 'news_db1', query=insertionCheckQuery)
print(records)"""