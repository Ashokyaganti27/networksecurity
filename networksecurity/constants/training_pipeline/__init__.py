import os

"""
    DEFINING COMMON CONSTANTS VARIABLE FOR TRAINING PIPELINE

"""
TARGET_COLUMN ="class"
PIPELINE_NAME:str ="networksecurity"
ARTIFACT_DIR:str ="Artifacts"
FILE_NAME:str ="PhisingData.csv"
TRAINE_FILE_NAME:str ="train.csv"
TEST_FILE_NAME:str ="test.csv"

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

"""
    DATTA INGESTION REALETD CONSTANTS 

"""
DATA_INGESTION_COLLECTION_NAME:str ="NetworkData"
DATA_INGESTION_DATABASE_NAME:str ="Ashok"
DATA_INGESTION_DIR_NAME:str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str ="feature_store"
DATA_INGESTION_INGESTED_DIR:str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


"""
    DATA VALIDATION CONSTANTS

"""

DATA_VALIDATION_DIR_NAME:str ="data_validation"
DATA_VALIDATION_VALID_DIR:str ="validate"
DATA_VALIDATION_INVALID_DIR:str ="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str ="drift_report"
DATA_VALIDATION_DRIFT_REPORT_DIR_FILENAME:str ="report.yaml"



"""
   DATA TRANSFORMATION CONSTANTS

"""

DATA_TRANSFORMATION_DIR:str ="data_transomation"

DATA_TRANSFORMATION_SUB_DIR:str ="transformed"

DATA_TRANSFORMATION_TRAIN_NUMPY_ARRAY:str ="train.npy"
DATA_TRANSFORMATION_TEST_NUMPY_ARRAY:str ="test.npy"





