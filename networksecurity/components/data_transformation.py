from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import os,sys
import numpy as np
import pandas as pd
from networksecurity.entity.artifact_entity import DataTransfirmationArtifact,DatavalidationArtifact
from networksecurity.entity.config_entity import DataTransformationconfig
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.utils.common import save_to_numpy_array
"""
IN MY DATASET THERE IS NO MISSING VALUES AND MY DATASET CLEAN 

AND ALSO IT NOT A IMBALANCED DATASET

"""


class DataTransformation:
    def __init__(self,data_validayion_artifact:DatavalidationArtifact,data_tranformation:DataTransformationconfig):

        self.data_validayion_artifact=data_validayion_artifact
        self.data_transformation=data_tranformation

    def initiate_data_transformation(self) -> DataTransfirmationArtifact:
        
        try:

            train_data_path=self.data_validayion_artifact.valid_train_file_path
            test_data_path=self.data_validayion_artifact.valid_test_file_path

            train_data=pd.read_csv(train_data_path)
            test_data=pd.read_csv(test_data_path)

            ## i checked my data there is index column that not necessary 

            train_data.drop("Index",axis=1,inplace=True)
            test_data.drop("Index",axis=1,inplace=True)

            ## my target column is binary and it containe 1 an -1 i convert that into 1,0

            train_data[TARGET_COLUMN]=np.where(train_data[TARGET_COLUMN]==1,1,0)
            test_data[TARGET_COLUMN]=np.where(test_data[TARGET_COLUMN]==1,1,0)
            
            ###saving the train data into numpy array

            dir_for_train=self.data_transformation.data_transformation_train_path

            dir_train=os.path.dirname(dir_for_train)

            os.makedirs(dir_train,exist_ok=True)

            save_to_numpy_array(train_data,self.data_transformation.data_transformation_train_path)


            ###saving the test data into numpy array

            save_to_numpy_array(test_data,self.data_transformation.data_transformation_test_path)
            

            data_transformation_artifact=DataTransfirmationArtifact(
                train_numpy_path=self.data_transformation.data_transformation_train_path,
                test_numpy_path=self.data_transformation.data_transformation_test_path
            )

            
            return data_transformation_artifact
        
        except Exception as e:
           raise NetworkSecurityException(e,sys)





        




