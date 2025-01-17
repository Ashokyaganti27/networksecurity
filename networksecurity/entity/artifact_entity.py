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
