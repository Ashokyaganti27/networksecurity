from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import Modeltrainer
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineconfi,DataValidationConfig,DataTransformationconfig,Modeltrainerconfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataTransfirmationArtifact,DatavalidationArtifact,ModelTrainerArtifact
from networksecurity.constants.training_pipeline import BUCKET_NAME,FINAL_MODEL
from networksecurity.cloud.s3_syncer import s3sync
import os

class TrainingPipeline:
    def __init__(self):
      self.training_pipeline_config=TrainingPipelineconfi()
      self.s3syncer=s3sync()

    

    def start_data_ingestion(self):
        try:  
           data_ingestion_config=DataIngestionConfig(training_pipelin_config=self.training_pipeline_config)
           data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
           logger.info("Initiate Data Ingestion")
           data_ingestion_artifact=data_ingestion.data_ingestion()
           logger.info("Data ingestion completed")

           return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            datavalidationconfig=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_validation_config=datavalidationconfig,data_ingestion_artifact=data_ingestion_artifact)
            logger.info("Data Validation Initiated")

            data_validation_artifact=data_validation.initiate_data_validation()
            logger.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
           raise NetworkSecurityException(e,sys)
       
    def start_data_transformartion(self,data_validation_artifact:DatavalidationArtifact):
        try:
            logger.info("Data Transformation Initiated")
            datatransformation=DataTransformationconfig(self.training_pipeline_config)
            datatransformation=DataTransformation(data_validayion_artifact=data_validation_artifact,data_tranformation=datatransformation)

            data_transformation_artifact=datatransformation.initiate_data_transformation()
            logger.info("Data Transformation Completed")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def start_model_trainer(self,data_transformation_artifact:DataTransfirmationArtifact)->ModelTrainerArtifact:
        try:
            logger.info("Model trainer Initiated")
            modeltransformation=Modeltrainerconfig(self.training_pipeline_config)
            model_trainer=Modeltrainer(data_tans_artifact=data_transformation_artifact,model_trainer_config=modeltransformation)

            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logger.info("Model Trainer Success")

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{BUCKET_NAME}/artifact/{self.training_pipeline_config.timestap}"
            self.s3syncer.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_final_model_to_s3(self):
        try:
            aws_bucket_url=f"s3://{BUCKET_NAME}/final_model/{self.training_pipeline_config.timestap}"

            self.s3syncer.sync_folder_to_s3(folder=FINAL_MODEL,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def run_pipeline(self)->ModelTrainerArtifact:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformartion(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_final_model_to_s3()

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)



if __name__=="__main__":
    training_object=TrainingPipeline()
    logger.info("Overall Training Started/")
    training_object.run_pipeline()
    logger.info("Training Pipeline completed")