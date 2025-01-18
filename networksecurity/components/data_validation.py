from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DatavalidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig,TrainingPipelineconfi
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logger
from networksecurity.utils.common import read_yaml_file,write_yaml_file
import pandas as pd
from scipy.stats import ks_2samp
import os,sys
import numpy as np

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:

        no_of_columns=len(self.schema["columns"])
        logger.info(f"required no of column :{no_of_columns}")
        logger.info(f"data frame  has :{len(dataframe.columns)} columns")
        
        if len(dataframe.columns)==no_of_columns:
            return True
        else:
            return False
        

    def no_of_numeric_columns(self,dataframe):

        list_of_numeric_columns=[]

        for column in dataframe.columns:
            if np.issubdtype(dataframe[column].dtype,np.integer) or np.issubdtype(dataframe[column].dtype,np.floating):
                list_of_numeric_columns.append(column)
        return list_of_numeric_columns

    def detect_datset_drift(self,base_df,current_df,threshold):
        
        status=True
        report={}
        drift_columns=[]
        for columns in base_df.columns:
            d1=base_df[columns]
            d2=current_df[columns]
            is_same_dist=ks_2samp(d1,d2) #### it used to check the drift
            is_found=threshold > is_same_dist.pvalue ### if p value less than threshold there is drift present
            status=status and not is_found
            report.update({columns:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
            }})
        drift_report_file_path=self.data_validation_config.drift_report_file_path
        dir_name=os.path.dirname(drift_report_file_path)

        os.makedirs(dir_name,exist_ok=True)

        write_yaml_file(filepath=drift_report_file_path,content=report)

        logger.info(f"No of drift columns are {len(drift_columns)} and they are {drift_columns}")

        return status



        
    def initiate_data_validation(self)->DatavalidationArtifact:
        try:

            train_file_path=self.data_ingestion_artifact.train_data_path
            test_file_path=self.data_ingestion_artifact.test_data_path

            ###read data from test and train

            train_data=pd.read_csv(train_file_path)
            test_data=pd.read_csv(test_file_path)

            ###validate no of columns

            if not self.validate_no_of_columns(train_data):
                logger.info("train data does not contain all columns")
                raise ValueError("Invalid No of columns in Train data")


            if not self.validate_no_of_columns(test_data):
                logger.info("test data does not contain all columns")
                raise ValueError("Invalid No Of columns in Test data")
            

            num_for_train=self.no_of_numeric_columns(train_data)

            if len(num_for_train)>0:
                logger.info("Numeric column are present in Train Data ")

            else:
                logger.info("Numeric column are not Present in Train Data")
            
            num_for_test=self.no_of_numeric_columns(test_data)
            if len(num_for_test)>0:
                logger.info("Numeric column are present in Test Data ")

            else:
                logger.info("Numeric column are not Present in Test Data")

            ###checking numeric column are equal in train and test

            if len(num_for_train)==len(num_for_test):
                logger.info("Numeric columns are equal in both train and test data")
            else:
                raise ValueError("Numeric Columns are not equal in Both train and test")

            



            ##lets check data drift
            status=self.detect_datset_drift(base_df=train_data,current_df=test_data,threshold=0.05)

            if status:
            
                dir_name=os.path.dirname(self.data_validation_config.train_valid_data_path)
                os.makedirs(dir_name,exist_ok=True)

                train_data.to_csv(
                    self.data_validation_config.train_valid_data_path,index=False,header=True)

                test_data.to_csv(
                    self.data_validation_config.test_valid_data_path,index=False,header=True)
                                

                data_validation_artifact=DatavalidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_validation_config.train_valid_data_path,
                    valid_test_file_path=self.data_validation_config.test_valid_data_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path

                )
                
                logger.info(f"status is {status} and these is validate path")


                return data_validation_artifact
            else:

                dir_name=os.path.dirname(self.data_validation_config.train_invalid_data_path)
                os.makedirs(dir_name,exist_ok=True)

                train_data.to_csv(
                    self.data_validation_config.train_invalid_data_path,index=False,header=True
                )
                 
                test_data.to_csv(
                    self.data_validation_config.test_invalid_data_path,index=False,header=True
                )

                data_validation_artifact=DatavalidationArtifact(
                    validation_status=status,
                    valid_train_file_path=None,
                    valid_test_file_path=None,
                    invalid_train_file_path=self.data_validation_config.train_invalid_data_path,
                    invalid_test_file_path=self.data_validation_config.test_invalid_data_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path

                )


                logger.info(f"status is {status} and these is invalid path")

                return data_validation_artifact


        except Exception as e:
           raise NetworkSecurityException(e,sys)
        
           
          











