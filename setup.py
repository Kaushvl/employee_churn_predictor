from setuptools import find_packages,setup
from typing import List

requirement_file_name = 'requirements.txt'
REMOVE_PACKAGE = '-e .'

def get_requirements(filepath:str)->List[str]:
    with open(filepath) as requirement_file:
        requirement_list = requirement_file.readline()
    requirement_list = [requirement_name.replace("\n","") for requirement_name in requirement_list]

    # if REMOVE_PACKAGE in requirement_list:
    #     requirement_list.remove(REMOVE_PACKAGE)
    return requirement_list

setup(
    name="ECP",
    version='0.0.1',
    description="Employee churn predictor",
    author="kaushal shukla",
    author_email='shukla.k@hotmail.com',
    packages=find_packages(),
    install_reqires=get_requirements(requirement_file_name)
    )