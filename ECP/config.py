import pymongo
import pandas as pd
import numpy as np
import json,os,sys

class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = 'Attrition'
print("env_var, mongo_db_url")