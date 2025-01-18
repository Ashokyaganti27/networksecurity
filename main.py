from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineconfi,DataValidationConfig,DataTransformationconfig

if __name__=="__main__":

    try:
        traing_config=TrainingPipelineconfi()
        dataingestionconfig=DataIngestionConfig(traing_config)
        dataingestion=DataIngestion(dataingestionconfig)
        logger.info("--Initiate Data Ingestion--")
        data_ingestion_artifact=dataingestion.data_ingestion()
        logger.info("Data Ingestion Completed")

        datavalidationconfig=DataValidationConfig(traing_config)
        data_validation=DataValidation(datavalidationconfig,data_ingestion_artifact)
        logger.info("Data Validation Initiated")
        data_validation_artifact=data_validation.initiate_data_validation()
        logger.info("Data validation completed")

        logger.info("Data Transformation Initiated")
        datatransformation=DataTransformationconfig(traing_config)
        datatransformation=DataTransformation(data_validayion_artifact=data_validation_artifact,data_tranformation=datatransformation)
        data_transformation_artifact=datatransformation.initiate_data_transformation()
        logger.info("Data Transformation Completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)


