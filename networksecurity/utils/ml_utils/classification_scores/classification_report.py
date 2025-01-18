from networksecurity.entity.artifact_entity import classificationmetricArtifact
from networksecurity.exceptions.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def get_classification_score(y_true,y_pred):
    try: 
       
       model_f1_score=f1_score(y_true,y_pred)
       model_recall_score=recall_score(y_true,y_pred)
       model_precision_score=precision_score(y_true,y_pred)

       classfication_artifact=classificationmetricArtifact(
              f1_score=model_f1_score,
              recall_score=model_recall_score,
              precision_score=model_precision_score
       )

       return classfication_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)

