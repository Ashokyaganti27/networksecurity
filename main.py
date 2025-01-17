from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineconfi

if __name__=="__main__":

    try:
        traing_config=TrainingPipelineconfi()
        dataingestionconfig=DataIngestionConfig(traing_config)
        dataingestion=DataIngestion(dataingestionconfig)
        logger.info("--Initiate Data Ingestion--")
        dataingestion.data_ingestion()
    except Exception as e:
        raise NetworkSecurityException(e,sys)


