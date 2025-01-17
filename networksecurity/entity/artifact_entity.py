from dataclasses import dataclass
from pathlib import Path

@dataclass
class Artifactconfig:
    train_data_path:str
    test_data_path:str


