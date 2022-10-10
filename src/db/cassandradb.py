import pandas as pd
import sys, os
from src.logger import logging
from src.exception import CustomException
from src.constants import *
from src.utils.util import read_yaml
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class DBOps:
    def __init__(self):
        try:
            self.auth_id = read_yaml(SECRET_PATH)[CASDB][ID]
            self.auth_secret = read_yaml(SECRET_PATH)[CASDB][SECRET]
            self.cloud_config = {'secure_connect_bundle': BUNDLE_PATH}
            self.keyspace = 'vox_news_summarizer'
        except Exception as e:
            raise CustomException(e, sys) from e

    def getCluster(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            cluster = Cluster(cloud=self.cloud_config, auth_provider=PlainTextAuthProvider(self.auth_id, self.auth_secret))
            return cluster
        except Exception as e:
            raise CustomException(e, sys) from e

    def closeSession(self, session):
        """
        This function closes the cluster connection
        """
        try:
            session.shutdown()
        except Exception as e:
            raise CustomException(e, sys) from e

    def createSession(self):
        """
        Create a cluster session
        """
        try:
            session = self.getCluster().connect()
            return session
        except Exception as e:
            raise CustomException(e, sys) from e

    def isTablePresent(self, table_name):
        """
        this function checks whether the table is available inside the keyspace
        """
        try:
            session = self.createSession()
            query = f"""
                SELECT * FROM system_schema.tables WHERE keyspace_name = '{self.keyspace}';
            """
            if table_name in [i[1] for i in session.execute(query)]:
                self.closeSession(session)
                return True
            else:
                self.closeSession(session)
                return False
        except Exception as e:
            raise CustomException(e, sys) from e

    def createTable(self, table_name):
        """
        Function creates a table using keyspace and table name
        """
        try:
            session = self.createSession()
            status = self.isTablePresent(table_name)
            if not status:
                query = f"""
                    CREATE TABLE IF NOT EXISTS {self.keyspace}.{table_name} (id uuid, date text, keyword text, headline text, summary text, PRIMARY KEY(id));
                """
                table = session.execute(query)
                self.closeSession(session)
                return table
            else:
                print(f'Table {table_name} already exists')
        except Exception as e:
            raise CustomException(e, sys) from e

    def insertOneRecord(self, table_name, values):
        """
        Function inserts one record into the table in keyspace
        """
        try:
            session = self.createSession()
            status = self.isTablePresent(table_name)
            table_key = "id, "+', '.join([str(i) for i in ['date', 'headline', 'keyword', 'summary']])
            values = "uuid(), "+", ".join([f"'{str(i)}'" for i in values])
            if status:
                query = f"""
                    INSERT INTO {self.keyspace}.{table_name}({table_key}) values ({values});     
                """
                print(query)
                session.execute(query)
                self.closeSession(session)
                print(f'record inserted into table {table_name} in keyspace {self.keyspace}')
            else:
                table = self.createTable(table_name)
                query = f"""INSERT INTO {self.keyspace}.{table_name}({table_key}) values ({values});"""
                print(query)
                session.execute(query)
                self.closeSession(session)
                print(f'record inserted into table {table_name} in keyspace {self.keyspace}')
        except Exception as e:
            raise CustomException(e, sys) from e

    def findAllRecords(self, table_name, date, keyword):
        """
        Function returns all the records in the table in the keyspace based on the query
        """
        try:
            session = self.createSession()
            status = self.isTablePresent(table_name)
            if status:
                query = f"SELECT * from {self.keyspace}.{table_name} where date='{date}' and keyword='{keyword}' ALLOW FILTERING;"
                print(query)
                rows = session.execute(query)
                self.closeSession(session)
                print(f'query was executed in {table_name} in keyspace {self.keyspace}')
                return [row for row in rows]
            else:
                table = self.createTable(table_name)
                query = f"SELECT * from {self.keyspace}.{table_name} where date='{date}' and keyword='{keyword}' ALLOW FILTERING;"
                rows = session.execute(query)
                self.closeSession(session)
                print(f'query was executed in {table_name} in keyspace {self.keyspace}')
                return [row for row in rows]
        except Exception as e:
            raise CustomException(e, sys) from e


if __name__ == '__main__':
    a = DBOps()
    print(a.findAllRecords('news', 'a', 'c'))

    