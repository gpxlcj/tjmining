#! -*- coding:utf-8 -*-
from django.views.decorators.cache import cache_page
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from project_lib.mongodb_mehtod import generate_limitation
from models import GeoMongoDBModel
from datetime import datetime
import time
from project_lib.build_json import render_to_json, return_status, return_error_status
from settings.origin import MONGO_CLIENT_IP, MONGO_CLIENT_PORT, MONGO_DB_NAME
from settings.origin import PLACE_PATTERN as place_pattern
import sys
import requests
import json


#--test--
import os, inspect


sys.path.append('/Users/gpxlcj/project/spark/python')
sys.path.append("/Users/gpxlcj/project/spark/python/lib")

from pyspark import SparkConf, SparkContext

import pymongo

@cache_page(1*1)
def heatmap_by_grid(request):

    return render_to_response('heatmapbygrid.html', locals())



def heatmap(request):
    print('func heatmap process')
    db_name = 'Y5bus'
    collection_name = 'GpsTaipei'

    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[collection_name]
    date_list = list()
    for i in range(1, 2):
        date_list.append({'Date': '2016-08-0'+str(i)})
    query_order = {'$or': date_list}
    raw_data = collection.find(query_order)

    if request.method == 'GET':
        data = list()
        for i in raw_data:
            temp_dict = dict()
            temp_dict['Latitude'] = i['Latitude']
            temp_dict['Longitude'] = i['Longitude']
            data.append(temp_dict)

        return render_to_response('trajectory/heatmap.html', locals())
    else:
        return Http404


def match_poi(lat, lon):

    url = 'http://nominatim.openstreetmap.org/reverse?lon='\
          +str(lon)+'&lat='+str(lat)+'&format=json&accept-language=en'
    req = requests.get(url)
    req = req.json()
    try:
        display_name = req['display_name']+u''
    except:
        display_name = u''
        req['display_name'] = u''
    try:
        address = str(req['address'])+u''
    except:
        req['address'] = u''

    return req


def generate_grid(max_lat, min_lat, max_lon, min_lon, lat_num, lon_num):

    print('func generate_grid process')
    d_lat = float(max_lat) - float(min_lat)
    d_lon = float(max_lon) - float(min_lon)
    lat_num = int(lat_num)
    lon_num = int(lon_num)
    lat_step = d_lat / lat_num
    lon_step = d_lon / lon_num
    temp_lat = max_lat
    temp_lon = min_lon
    data_list = list()
    for j in range(1, lat_num+1):
        for i in range(1, lon_num+1):
            temp_dict = dict()
            temp_dict['min_lat'] = temp_lat - j * lat_step
            temp_dict['max_lat'] = temp_lat - (j-1) * lat_step
            temp_dict['min_lon'] = temp_lon + (i-1) * lon_step
            temp_dict['max_lon'] = temp_lon + i * lon_step
            data_list.append(temp_dict)
    return data_list


def count_num_by_grid(data):
    pass


def count_point(collection_name, grid_list, sc=None):

    print('func count_point process')
    client = pymongo.MongoClient(MONGO_CLIENT_IP, MONGO_CLIENT_PORT)
    db = client[MONGO_DB_NAME]
    raw_data = db[collection_name]
    date_list = list()
    for i in range(1, 32):
        if i>9:
            date_list.append({'Date': '2016-08-0'+str(i)})
        else:
            date_list.append({'Date': '2016-08-'+str(i)})
    query_order = {'$or': date_list}
#test
    data = raw_data.find()

#    sc.parallelize(data, 10)

    temp_list = list()
    for j in grid_list:
        j['count'] = 0
        temp_list.append(j)
    count_list = temp_list

    for i in data:
        for j in count_list:
            if (float(i['Latitude']) < j['max_lat']) and (float(i['Latitude']) > j['min_lat']) and (float(i['Longitude']) < j['max_lon']) and (float(i['Longitude']) > j['min_lon']):
                j['count'] += 1
                break
            else:
                continue
    return count_list


def return_grid_count(num, count_list):

    print('func return_grid_count process')
    count_list = sorted(count_list, key=lambda k: k['count'], reverse=True)
    if (num != 0) and (len(count_list)>num):
        count_list = count_list[:num]
    for i, grid in enumerate(count_list):
        if grid['count']>10:
            continue
        else:
            break
    count_list = count_list[:i]
    return count_list


def return_grid_poi(num, count_list):

    print('func return_grid_poi process')
    count_list = sorted(count_list, key=lambda k: k['count'], reverse=True)
    if (num != 0) and (len(count_list)>num):
        count_list = count_list[:num]
    for i, grid in enumerate(count_list):
        if grid['count']>100:
            continue
        else:
            break
    count_list = count_list[:i]
    for grid in count_list:
        latitude = (grid['max_lat'] + grid['min_lat']) / 2
        longitude = (grid['max_lon'] + grid['min_lon']) / 2
        poi_info = match_poi(latitude, longitude)
        grid['poi_info'] = poi_info
    return count_list


#api
@cache_page(60 * 1)
def get_hot_region(request):
    if request.method == 'GET':

#        conf = (SparkConf().setMaster('local').setAppName('MyApp').set('spark.executor.memory', '1g'))
#        sc = SparkContext(conf = conf)

        data = dict()
        try:
            database_id = request.GET['database_id']
            geo_mongo = GeoMongoDBModel.objects.get(db_id=database_id)
        except:
            error_info = 'database_id is wrong or blank'
            return render_to_json(return_error_status('500', error_info))

        if request.GET.has_key('method'):
            p_method = request.GET['method']

# heatmap method
            if p_method == 'heatmap':
                temp_data = return_status('200')
                return heatmap(request)

# grid method
            elif p_method == 'grid':
                if not geo_mongo.is_modified:
                    generate_limitation(database_id)
                else:
                    pass

                try:
                    latitude_num = float(request.GET['latitude_num'])
                except:
                    latitude_num = 10
                try:
                    longitude_num = float(request.GET['longitude_num'])
                except:
                    longitude_num = 10
                grid_list = generate_grid(geo_mongo.max_latitude, geo_mongo.min_latitude,
                                          geo_mongo.max_longitude, geo_mongo.min_longitude,
                                          latitude_num, longitude_num)
                count_list = count_point(geo_mongo.collection_name, grid_list)

                try:
                    resp_type = int(request.GET['resp_type'])
                except:
                    resp_type = 1

                try:
                    resp_num = int(request.GET['resp_num'])
                except:
                    resp_num = 10

                temp_data = return_status('200')
                if resp_type == 1:
                    count_list = return_grid_count(resp_num, count_list)
                    temp_data['grid_list'] = count_list
                elif resp_type == 2:
                    poi_list = return_grid_poi(resp_num, count_list)
                    temp_data['grid_list'] = poi_list


# clustering method
            elif p_method == 'clustering':
                temp_data = return_status('200')

# method unavailable
            else:
                error_info = 'the method is unavailable'
                temp_data = return_error_status('500', error_info)
        else:
            error_info = 'please offer one method'
            temp_data = return_error_status('500', error_info)

        data = temp_data

#        sc.stop()
        return render_to_json(data)
    else:
        return Http404


#------------------------------  visulization test part START  ---------------
def visual_data_transfer(raw_data):
    point_list = list()
    data = {
        'type': 'FeatureCollection',
        'features': point_list,
    }
    for i, dict_i in enumerate(raw_data):
        print(dict_i)
        x_lat = dict_i['max_lat']
        n_lat = dict_i['min_lat']
        x_lon = dict_i['max_lon']
        n_lon = dict_i['min_lon']
        temp_data = dict()
        properties = dict()
        temp_data['properties'] = properties
        geometry = dict()
        temp_data['geometry'] = geometry
        temp_data['type'] = 'Feature'
        temp_data['id'] = str(i)
        properties['density'] = dict_i['count']

        try:
            properties['name'] = dict_i['poi_info']['display_name']
        except:
            properties['name'] = 'where?'

        geometry['type'] = 'Polygon'
        geometry['coordinates'] = [[[n_lon, x_lat], [x_lon, x_lat], [x_lon, n_lat], [n_lon, n_lat]]]
        point_list.append(temp_data)

    print(data)
    return data

def display_level(data):
    last_temp = -1
    dif_list = list()
    for i,d in enumerate(data):
        temp = d['properties']['density']
        if last_temp>0:
            temp = last_temp - temp
            temp_dict = {'value':temp, 'num':i}
            dif_list.append(temp_dict)
        last_temp = temp
    order_list = sorted(dif_list, key=lambda k: k['value'], reverse=True)
    if len(order_list)>6:
        range_num = 7
    else:
        range_num = len(order_list)
    ans_list = list()
    for i in range(range_num):
        num = order_list[i]['num']
        ans_list.append(data[num]['properties']['density'])
    ans_list = sorted(ans_list, reverse=True)
    return ans_list



#web
def show_hot_region(request):
    base_url = 'http://127.0.0.1:8000'
    data_url = base_url + '/hotregion/get_hot_region'
    print(data_url)
    r_data = {
        'database_id': '1483372489511521062',
        'method':'grid',
        'resp_type':2,
        'resp_num':0,
        'latitude_num': 80,
        'longitude_num': 40
    }
    data = requests.get(data_url, params = r_data)
    print(data.json())
    data = data.json()
    try:
        data = data['grid_list']
    except:
        return render_to_response('heatmapbygrid_2.html', locals())
# store hot region grid into database
#    client = pymongo.MongoClient('localhost', 27017)
#    db_name = 'Y5bus'
#    db = client[db_name]
#    col_grid = db['HotRegion']
#    for i in data:
#        col_grid.insert(i)


# store end

    data = visual_data_transfer(data)
    data_file = 'djs_'+str(time.time())+'.js'
    level_list = display_level(data['features'])
    level_list_reverse = list(level_list)
    level_list_reverse.reverse()
# -- file path --
    ta = inspect.getfile(inspect.currentframe())
    tb = os.path.abspath(ta)
    tc = os.path.dirname(tb)
    print(tc)
    static_file_path = tc+'/../../static/data_hot/'
# -- file path END --
    jsf = open(static_file_path+data_file, 'w')
    jsf.write('var statesData =')
    try:
        data = json.dumps(data)
    except:
        print(data)
        return render_to_response('blog/index.html', locals())
    jsf.writelines(data)
    jsf.close()
    return render_to_response('heatmapbygrid.html', locals())


#------------------------------  visulization test part END  ---------------

#---------------------- caculate time between hotregion --------------

def find_trajectory(request):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db_name = 'Y5bus'
    db = client[db_name]
    collection_name = 'HotRegion'
    grid_c = db[collection_name]
    grid_data = grid_c.find()
    collection_name = 'BusName'
    bus_c = db[collection_name]
    bus_data = bus_c.find()[:10]
    collection_name = 'BGps01_01'
    gps_data = db[collection_name]
    for bus_name in bus_data:
        gps_data = gps_data.find({'MacAddress': bus_name['MacAddress']})
        start_grid = -1
        end_grid = -1
        for i in gps_data:
            for grid in grid_data:
                if (float(i['Latitude']) < grid['max_lat']) and (float(i['Latitude']) > grid['min_lat']) and (
                    float(i['Longitude']) < grid['max_lon']) and (float(i['Longitude']) > grid['min_lon']):
                    temp_grid = grid['num_id']
                    if start_grid == -1:
                        start_grid = temp_grid
                else:
                    temp_grid = -1
        





def caculate_time(data, addr_list):

    pass

#---------------------- caculate END ---------------------------------


#---------- test -----------------

def sample_show(request):
    return render_to_response('heatmapbygrid_2.html', locals())

#---------- test END -------------