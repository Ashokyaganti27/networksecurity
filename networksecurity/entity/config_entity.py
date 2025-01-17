from datetime import datetime
import os

from networksecurity.constants import training_pipeline


class TrainingPipelineconfi:
    def __init__(self,timestap=datetime.now()):
        timestap=timestap.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestap)
        self.timestap:str =timestap

class DataIngestionConfig:
    def __init__(self,training_pipelin_config:TrainingPipelineconfi):
        self.data_ingestion_dir:str =os.path.join(
            training_pipelin_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        
        self.feature_store_file_path=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        
        self.training_file_path=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAINE_FILE_NAME
        )


        self.testing_file_path=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME
        )


        self.train_test_split_ratio:float =training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.data_ingestion_collection_name:str =training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.data_ingestion_database_name:str =training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,trainigpipelineconfig:TrainingPipelineconfi):

        self.data_validation_dir:str = os.path.join(trainigpipelineconfig.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.train_valid_data_path:str = os.path.join(self.valid_data_dir,training_pipeline.TRAINE_FILE_NAME)
        self.test_valid_data_path:str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.train_invalid_data_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TRAINE_FILE_NAME)
        self.test_invalid_data_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)

        self.drift_report_file_path=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR_FILENAME
        )
        

        



