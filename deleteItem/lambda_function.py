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
import firebase_admin
from firebase_admin import auth, credentials
import boto3
def get_firebase_secret():
    client = boto3.client('ssm', region_name = 'us-east-1')
    parameter_name = "firebase-service-account"
    response = client.get_parameter(Name=parameter_name,WithDecryption=True)
    return json.loads(response["Parameter"]["Value"])
def lambda_handler(event, context):
    # Connect to mongodb
    uri = os.environ['mongouri']
    client = MongoClient(uri)
    db = client["MyDataBase"]
    collection = db["UserData"]
    # id_token = event['headers']['id_token']
    cors_headers = {
                "Access-Control-Allow-Origin":'*',
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
                "Access-Control-Allow-Headers": "Content-Type"
    }
    firebase_secret = get_firebase_secret()
    # print(firebase_secret)
    if(not firebase_admin._apps):
        cred = credentials.Certificate(firebase_secret)
        firebase_admin.initialize_app(cred)
    print(event)
    auth_header = event['headers']['Authorization']
    if(auth_header.split(" ")[0] == "Bearer"):
        id_token = auth_header[7:]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        body = json.loads(event['body'])
        collection.delete_one({"userId":uid,
                               "itemId":body["itemId"],
                               "imageUrl":body["imageUrl"],
                               "title":body["title"],
                               "new_price":body["new_price"],
                               "old_price":body["old_price"],
                               "discount_price":body["discount_price"],
                               "shipping_cost":body["shipping_cost"],
                               "coupons":body["coupons"],
                               "itemUrl":body["itemUrl"],
                               "discount_percent":body["discount_percent"]
                               })
        return{
            "statusCode":200,
            "headers":cors_headers,
        "body": json.dumps({"message":"Item successfully deleted"})
        }
    else:
        return {
            "statusCode": 401, 
            "headers": cors_headers,
            "body": json.dumps({"message": "Unauthorized access or invalid token format"})
        }
