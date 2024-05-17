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
import time
import base64
def get_token():
    # eBay OAuth token endpoint
    oauth_url = "https://api.ebay.com/identity/v1/oauth2/token"

    #client ID and client secret from eBay application
    client_id = os.environ["client_id"]
    client_secret = os.environ["client_secret"]

    # Encode client ID and secret in Base64
    basic_auth_str = f"{client_id}:{client_secret}"
    basic_auth_bytes = basic_auth_str.encode('utf-8')
    basic_auth_encoded = base64.b64encode(basic_auth_bytes).decode('utf-8')

    # HTTP headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth_encoded}"
    }

    # Request body with grant type and scope(s)
    request_body = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    # Make the POST request to obtain OAuth token
    response = requests.post(oauth_url, headers=headers, data=request_body)

    # Check if the request was successful
    if response.status_code == 200:
        oauth_token = response.json().get('access_token')
        return oauth_token
    else:
        # Handle errors and display the response
        print("Error:", response.status_code, response.text)
        return None
    
def lambda_handler(event, context):

    # Connect to mongodb
    # uri = "mongodb+srv://situjiachang:sGpDBMUDwntLjyfV@cluster0.yicme3k.mongodb.net/"
    # client = MongoClient(uri)
    # db = client["MyDataBase"]
    # collection = db["EbayData"]
    # print(event)
    oauth_token = get_token()
    ebay_api_endpoint = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    search_query = event["queryStringParameters"]["search_query"]
    result_limit = "200"
    params = {
              "q":search_query,
              'auto_correct': 'KEYWORD',
              "limit": result_limit
              }
    headers = {"Authorization": f"Bearer {oauth_token}"}
    response = requests.get(ebay_api_endpoint, headers=headers, params = params)
    discount_items = []
    cors_headers = {
                "Access-Control-Allow-Origin": 'http://localhost:3000',
                "Access-Control-Allow-Methods": "GET, POST, PUT,DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
    }
    if response.status_code == 200:

        data = response.json()
        # print(item["marketingPrice"]["discountPercentage"])
        # print(item["marketingPrice"]["discountAmount"])
        # print(item["itemWebUrl"])

        if("itemSummaries" in data):
            discount_items = [item for item in data["itemSummaries"] if "marketingPrice" in item]
            for item in data["itemSummaries"]:
                if("image" not in item and "thumbnailImages" not in item):
                    if("additionalImages" not in item):
                        print(item)
        else:
            return{
                "statusCode":"200",
                "headers":cors_headers,
            "body": json.dumps([])
            }
    # Make the GET request to fetch item details
        # headers = {"Authorization": f"Bearer {oauth_token}"}
        # for item_id in item_ids:
        #     ebay_item_endpoint = f"https://api.ebay.com/buy/browse/v1/item/v1|{item_id}|0"
        #     item_response = requests.get(ebay_item_endpoint, headers=headers)

        #     if item_response.status_code == 200:
        #         item_info = item_response.json()
        #         print("Item Details:", item_info)
        #     else:
        #         print("Error retrieving item details:", item_response.status_code, item_response.json())
        # for item in items:
        #     curr_price = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
        #     item_id = item["itemId"][0]
        #     image_url = item["galleryURL"][0]
            # collection.update_one({"itemId":item_id, "imageURL":image_url}, {"$set": {"price":curr_price}}, upsert=True)
        return {
            "statusCode": 200,
            "headers":cors_headers,
            "body": json.dumps(discount_items)
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": "Error fetching data"
        }