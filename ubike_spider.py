#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import post, get
from collections import defaultdict, OrderedDict
import json 
import secret
import utils
from ubike_exception import UbikeError
import time

class UbikeManager(object):
    ''' 
        Data that could share for other thread or process.
    '''
    crawl_data = defaultdict(dict) 
    api_url = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=ddb80380-f1b3-4f8e-8016-7ed9cba571d5'

    def __init__(self):
        '''Init the crawl_data'''
        self.crawl_ubikes()

    def get_location_info(self, lat, lng):
        '''
            Use googleapis to check location information and 
            the correctness of lat, lng .
        '''
        rsp = get('https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={key}'.format(lat=lat, lng=lng, key=secret.key))
        rsp_json = rsp.json()
        status = rsp_json['status']
        if status != 'OK':
            raise UbikeError(-1) 
        city = rsp_json['results'][0]['address_components'][-3]['short_name']
        print city
        if city == 'Taipei City':
            return self.get_neighbor(lat, lng)
        else:
            raise UbikeError(-2)
    
    def check_full(self):
        '''
            Check the ubike station is full or not.
            Raise exception when full.
        '''
        ubike_full = all(v['num_empty'] > 0 for v in self.crawl_data.values())
        for i, v in self.crawl_data.items():
            print i, v['num_empty']
        if ubike_full == 0:
            raise UbikeError(1)

    def get_neighbor(self, lat, lng): 
        '''
            rtype: tuple(error, json(result))
            Find the nearest station by calculate distance from lat, lng
        '''
        self.check_full()
        dist_dict = {i:utils.haversine(self.crawl_data[i]['latlng'] ,float(lat), float(lng)) \
                for i in self.crawl_data if self.crawl_data[i]['num_ubike']}
        sort_dict = OrderedDict(sorted(dist_dict.items(), key=lambda t: t[1]))
        near_station = []
        for idx in sort_dict:
            print self.crawl_data[idx]['sna']
        for idx in sort_dict:
            Order = {'station':self.crawl_data[idx]['sna'], 'num_ubike':self.crawl_data[idx]['num_ubike']}
            near_station.append(Order)
            if len(near_station) == 2:
                return (0, json.dumps(near_station, ensure_ascii=False,indent=-1))

    def crawl_ubikes(self):
        '''
            Use requests modules to get the ubike api json.
        '''
        rep = get(self.api_url)
        if rep.status_code != 200:
            raise UbikeError(3)
        rep_json = rep.json() 
        for v in rep_json['result']['results']:
            self.crawl_data[v['_id']].update({
                'sna': v['sna'].encode('utf-8'),
                'num_ubike': int(v['sbi']),
                'num_empty': int(v['bemp']),
                'latlng': (float(v['lat']), float(v['lng'])),
                'sarea': v['sarea'].encode('utf-8')
            })
    
    @classmethod
    def update_num(cls):
        '''
            Crawl data periodly(45sec) by threading, use the class variable 
            and classmethod to update cached data.
        '''
        while True:
            print "Update_data"
            print cls.crawl_data
            time.sleep(45) 
            rep = get(cls.api_url)
            if rep.status_code != 200:
                raise UbikeError(3)
            rep_json = rep.json()
            for v in rep_json['result']['results']:
                cls.crawl_data[v['_id']]['num_ubike'] = int(v['sbi'])
                cls.crawl_data[v['_id']]['num_empty'] = int(v['bemp'])

if __name__ == "__main__":
    ubm = UbikeManager()
    print ubm.get_near_info(25.034153, 121.568509)
    
