from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DatavalidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig,TrainingPipelineconfi
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logger
from networksecurity.utils.common import read_yaml_file,write_yaml_file
import pandas as pd
from scipy.stats import ks_2samp
import os,sys

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
        logger.info(f"data frame has :{len(dataframe.columns)} columns")
        
        if len(dataframe.columns)==no_of_columns:
            return True
        else:
            return False
    def detect_datset_drift(self,base_df,current_df,threshold):
        
        status=True
        report={}
        for columns in base_df.columns:
            d1=base_df[columns]
            d2=current_df[columns]
            is_same_dist=ks_2samp(d1,d2)
            if threshold<=is_same_dist.pvalue:
                is_found=False
            else:
                is_found=True
                status=False
            report.update({columns:{
                "p_value":float(is_same_dist.pvalue),
                "drift_statu":is_found
            }})
        drift_report_file_path=self.data_validation_config.drift_report_file_path
        dir_name=os.path.dirname(drift_report_file_path)

        os.makedirs(dir_name,exist_ok=True)

        write_yaml_file(filepath=drift_report_file_path,content=report)



        
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


            if not self.validate_no_of_columns(test_data):
                logger.info("test data does not contain all columns")


            ##lets check data drift
            status=self.detect_datset_drift(base_df=train_data,current_df=test_data,threshold=0.05)
            
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

            return data_validation_artifact
        except Exception as e:
           raise NetworkSecurityException(e,sys)
        
           
          











