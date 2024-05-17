import numpy as np
import pandas as pd
import json
import requests
import urllib.parse
import urllib.request
import os
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import base64

    
def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps(None)}