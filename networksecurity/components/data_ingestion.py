from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

####configuration of the Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import Artifactconfig
import os
import sys
import pymongo
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split # type: ignore
from dotenv import load_dotenv 
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def import_data_from_mongodb(self):

        try:
            self.database=self.data_ingestion_config.data_ingestion_database_name
            self.collection=self.data_ingestion_config.data_ingestion_collection_name
            self.pymongo_client=pymongo.MongoClient(MONGO_DB_URL)

            collection=self.pymongo_client[self.database][self.collection]
            dataframe=pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns.to_list():
                dataframe=dataframe.drop(columns=["_id"],axis=1)

            return dataframe

        except Exception as e:  
            raise NetworkSecurityException(e,sys)

    def export_data_into_featue_store(self,dataframe:pd.DataFrame):
        try:
            
            feature_store_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_path)

            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_path,index=False,header=True)

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe:pd.DataFrame):

        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            
            logger.info("performed train test split on the dataframe")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logger.info("svaing train data and test data to their directories")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True)
            
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True)
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    

    def data_ingestion(self):
        try:
            dataframe=self.import_data_from_mongodb()
            data=self.export_data_into_featue_store(dataframe)
            self.split_data_as_train_test(data)

            artifactdataconfig=Artifactconfig(
                train_data_path=self.data_ingestion_config.training_file_path,
                test_data_path=self.data_ingestion_config.testing_file_path

            )
             
            return artifactdataconfig

        except Exception as e:
            raise NetworkSecurityException(e,sys)





