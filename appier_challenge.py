#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, request
import ubike_spider
import threading
from ubike_exception import UbikeError
app = Flask(__name__)

@app.route('/v1/ubike-station/taipei')
def bike_in_taipei():
    '''
        Primary method to parse url and get args for the infomation.
    '''
    args = request.args.to_dict()
    if 'lat' in args and 'lng' in args:
        try:
            return respon(*UBM.get_location_info(args['lat'], args['lng']))
        except UbikeError as e:
            return respon(e.value)
    else:
        return respon(-3)

@app.errorhandler(404)
def system_error(e):
    '''
        Handle the url which not found.
    '''
    return respon(-3)

def respon(error, result=None):
    '''
        Use to return json file.
    '''
    if not result:
        result = []
    resp = {
        "code": error,
        "result": result
        }
    print resp
    resp_json = jsonify(resp)
    return resp_json

if __name__ == "__main__":
#    query_url = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=ddb80380-f1b3-4f8e-8016-7ed9cba571d5'
    UBM = ubike_spider.UbikeManager()
    backcrawl = threading.Thread(target=UBM.update_num)
    backcrawl.daemon = True
    backcrawl.start()
    app.run(host='0.0.0.0', port=1234)

