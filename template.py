import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')



list_of_files=[
    ".github/workflows/main.yaml",
    "networksecurity/__init__.py",
    "networksecurity/constants/__init__.py",
    "networksecurity/utils/__init__.py",
    "networksecurity/entity/__init__.py",
    "networksecurity/components/__init__.py",
    "networksecurity/pipeline/__init__.py",
    "networksecurity/config/__init__.py",
    "networksecurity/logging/__init__.py",
    "networksecurity/logging/logger.py",
    "networksecurity/exceptions/__init__.py",
    "networksecurity/exceptions/exception.py",
    "setup.py",
    "DockerFile",
]


for files in list_of_files:
    filepath=Path(files)
    filedir,filename=os.path.split(filepath)


    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"filediectory successfully created at {filepath}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)):

        with open(filepath,"w") as file:
            pass
        logging.info(f"filename successfully created at {filepath}")
    else:
        logging.info(f"filename already exists {filename}")






