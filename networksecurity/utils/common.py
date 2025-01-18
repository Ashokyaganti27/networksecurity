import yaml
import os
import sys
from networksecurity.exceptions.exception import NetworkSecurityException
import numpy as np
def read_yaml_file(filepath:str) ->dict:
    try:
        with open(filepath,"rb") as yamlfile:
            return yaml.safe_load(yamlfile)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml_file(filepath: str, content: dict):
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


