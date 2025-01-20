from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import pandas as pd
import os,sys
from networksecurity.entity.artifact_entity import DataTransfirmationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import Modeltrainerconfig
from networksecurity.utils.ml_utils.classification_scores.classification_report import get_classification_score
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
from networksecurity.utils.common import evaluate_model
import pickle
import mlflow

import dagshub
dagshub.init(repo_owner='YagantiAshok177', repo_name='networksecurity', mlflow=True)

class Modeltrainer:
    def __init__(self,data_tans_artifact:DataTransfirmationArtifact,model_trainer_config:Modeltrainerconfig):

        try:
            self.data_trans_artifact=data_tans_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    


    def track_mlflow(self,best_model,classification_report):

        mlflow.set_experiment("NetWorkSecurity_Models")  
        with mlflow.start_run():

            f1_score=classification_report.f1_score
            precision=classification_report.precision_score
            recall_score=classification_report.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision)
            mlflow.log_metric("recall",recall_score)

            mlflow.sklearn.log_model(best_model,"model")


    def train_model(self,x_train,y_train,x_test,y_test):
        try:

            models={
              "LogisticRegression":LogisticRegression(),
              "DecisionTreeClassifier":DecisionTreeClassifier(),
              "AdaBoostClassifier":AdaBoostClassifier(),
              "GradientBoostingClassifier":GradientBoostingClassifier(),
              "RandomForestClassifier":RandomForestClassifier()
            }

            report:dict =evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)

            best_model_score=max(sorted(report.values()))

            best_model_name=list(report.keys())[
                list(report.values()).index(best_model_score)
            ]
            

            best_model=models[best_model_name]

            logger.info(f"best model is {best_model_name}")

            y_train_pred=best_model.predict(x_train)

            classification_xtrain_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            logger.info("classification report for train data success")



            y_test_pred=best_model.predict(x_test)

            classification_xtest_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            logger.info("classification report for test data success")


            ####mlflow tracking 


            self.track_mlflow(best_model=best_model,classification_report=classification_xtest_metric)


            dir_name=self.model_trainer_config.model_name_path

            path=os.path.dirname(dir_name)
            
            os.makedirs(path,exist_ok=True)

            logger.info("model.pkl path created successfully")

            with open(self.model_trainer_config.model_name_path,"wb") as file:
                pickle.dump(best_model,file)

            ##saving into final_model
            os.makedirs("final_model",exist_ok=True)
            with open("final_model/model.pkl","wb") as file:
                pickle.dump(best_model,file)
                file.close()


            
            model_trainer_artifact=ModelTrainerArtifact(
                model_trained_path=self.model_trainer_config.model_name_path,
                train_metric_artifact=classification_xtrain_metric,
                test_metric_artifact=classification_xtest_metric
            )
            

            return model_trainer_artifact
          
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
    
        try:

        ###take and load the data from datatransartifact

            train_data=np.load(self.data_trans_artifact.train_numpy_path)
            test_data=np.load(self.data_trans_artifact.test_numpy_path)

            ###dividing train  data into input features and output features


            train_data_x=train_data[:,:-1]##get all the column data witout last column
            train_data_y=train_data[:,-1]##get last column data

            ###dividing test  data into input features and output features

            test_data_x=test_data[:,:-1]
            test_data_y=test_data[:,-1]

            model_trainer_artifact=self.train_model(x_train=train_data_x,y_train=train_data_y,x_test=test_data_x,y_test=test_data_y)

            logger.info("model trainer artifact ready")

            return model_trainer_artifact
        

        except Exception as e:
             raise NetworkSecurityException(e,sys)

    


