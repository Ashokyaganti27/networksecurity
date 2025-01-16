from setuptools import find_packages,setup
from typing import List
 

def requirements() ->List[str]:
    
    list_of_requirements:List[str]=[]

    """ these function return list of
        requirements
    """
    try:
        with open("requirements.txt","r") as file:
            #reading all lines from requirements.txt
            lines=file.readlines()

            for line in lines:
                ##removing all whitespaces and also new line characters
                requirement=line.strip()
                
                ##ignore empty lines and -e.
                if requirement!="" and requirement!= "-e .":
                    list_of_requirements.append(requirement)

    except FileNotFoundError:
        print("requirements File does not exists in these location")
    
    return list_of_requirements


setup(
    name="NetWorkSecurity",
    version="0.0.1",
    author="Yaganti Ashok",
    author_email="yagantiashok177@gmail.com",
    packages=find_packages(),
    install_requires=requirements()
)

