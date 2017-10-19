 
import pandas as pd
import numpy as np
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING

def get_db(database):
    """
    A quick way to get MongoDb Client link
    """
    clientmg=MongoClient()
    db=clientmg[database]
    return db

def seenan(input_value):
    try:
        if np.isnan(input_value):
            return False
        else:
            return True
    except:
        return True
