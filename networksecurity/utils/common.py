import yaml
import os
import sys
from networksecurity.exceptions.exception import NetworkSecurityException
import numpy as np
from sklearn.metrics import accuracy_score
from networksecurity.logging.logger import logger
def read_yaml_file(filepath:str) ->dict:
    try:
        with open(filepath,"rb") as yamlfile:
            return yaml.safe_load(yamlfile)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml_file(filepath: str, content):
    try:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
        
        with open(filepath, "w") as yamlfile:
            yaml.dump(content, yamlfile)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_to_numpy_array(dataframe,path):
    try:
        data=dataframe.to_numpy()

        np.save(path,data)

    except Exception as e:
       raise NetworkSecurityException(e,sys)


def evaluate_model(x_train,y_train,x_test,y_test,models):
    try:
        report={}

        for i in range(len(models)):

            model=list(models.values())[i]

            model.fit(x_train,y_train)


            y_test_pred=model.predict(x_test)


            test_model_score=accuracy_score(y_test,y_test_pred)

            report[list(models.keys())[i]]=test_model_score
            
            logger.info("report file succefully updated")

        return report

    except Exception as e:
         raise NetworkSecurityException(e,sys)
