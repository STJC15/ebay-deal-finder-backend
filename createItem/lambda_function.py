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

def lambda_handler(event, context):
    # Connect to mongodb
    uri = "mongodb+srv://situjiachang:sGpDBMUDwntLjyfV@cluster0.yicme3k.mongodb.net/"
    client = MongoClient(uri)
    db = client["MyDataBase"]
    collection = db["UserData"]
    print(event)
    return {'statusCode':200}