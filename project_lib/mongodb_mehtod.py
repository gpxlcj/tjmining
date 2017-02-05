#! -*- coding:utf-8 -*-
import pymongo
from apps.hotrigion.models import GeoMongoDBModel


def generate_limitation(db_id):
    geo_mongo = GeoMongoDBModel.objects.get(db_id = db_id)
    db_name = 'Y5bus'
    collection_name = geo_mongo.collection_name

    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[collection_name]
    raw_data = collection.find()
    max_longitude = -1
    min_longitude = 181
    max_latitude = -91
    min_latitude = 91
    for i in raw_data:
        latitude = float(i['Latitude'])
        longitude = float(i['Longitude'])
        if latitude and longitude:
            if latitude > max_latitude:
                max_latitude = latitude
            if latitude < min_latitude:
                min_latitude = latitude
            if longitude > max_longitude:
                max_longitude = longitude
            if longitude < min_longitude:
                min_longitude = longitude
        else:
            continue
    else:
        geo_mongo.max_latitude = max_latitude
        geo_mongo.min_latitude = min_latitude
        geo_mongo.max_longitude = max_longitude
        geo_mongo.min_longitude = min_longitude
        geo_mongo.is_modified = True
        geo_mongo.save()

