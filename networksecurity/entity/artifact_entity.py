from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    train_data_path:str
    test_data_path:str

@dataclass
class DatavalidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransfirmationArtifact:
    train_numpy_path:str
    test_numpy_path:str


@dataclass
class classificationmetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    model_trained_path:str
    train_metric_artifact: classificationmetricArtifact
    test_metric_artifact: classificationmetricArtifact