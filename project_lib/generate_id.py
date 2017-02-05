#! -*- coding:utf-8 -*-
from random import randint
import time
import pymongo

def generate_id():
    c = randint(5, 20)

    ans = str(int(round(time.time()*1000)))
    for i in range(0, c):
        ans += str(randint(1, 10))
    return ans


def add_order_to_grid():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db_name = 'Y5bus'
    db = client[db_name]
    collection_name = 'HotRegion'
    grid_c = db[collection_name]
    grid_data = grid_c.find()
    for i, grid in enumerate(grid_data):
        grid_c.update({'_id':grid['_id']}, {'$set':{'num_id': i}})
