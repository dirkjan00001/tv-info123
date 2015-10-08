#!/usr/bin/env python

import json
from datetime import datetime
import time

try:
    from urllib.request import urlopen      # For Python 3.0 and later
except ImportError:
    from urllib2 import urlopen             # Fall back to Python 2's urllib2

class info123:
    def __init__(self, channelstring = "1,2,3"):
        self.data = []
        self.json_url = "http://www.tvgids.nl/json/lists/programs.php?channels=%s" %channelstring
        self.cache_filename = "cache.json"

    def update(self, enable_caching = True):
        if enable_caching == True and self.json_read_file():
            return  #data successfully read from file
        response = urlopen(self.json_url)       # TODO create something with a timeout
        json_data = response.read()
        if enable_caching:
            self.json_write_file(json_data)         # write the data to a file
        self.data = json.loads(json_data)

    def get_current_program(self, channel):
        return self.get_program(datetime.now(), channel)

    def get_program(self, datetime_prog, channel):
        # format:
        # u'datum_end': u'2015-10-01 00:15:00',
        # u'datum_start': u'2015-09-30 23:55:00',
        # u'db_id': u'19081949',
        # u'genre': u'Nieuws/actualiteiten',
        # u'kijkwijzer': u'',
        # u'soort': u'Nieuwsbulletin',
        # u'titel': u'Journaal'}]
        channel_info = self.data[channel]

        if isinstance(channel_info, dict):
            channel_info_list = channel_info.values()
        else:
            channel_info_list = channel_info

        for program in channel_info_list:
            datetime_start = self.strip_time(program['datum_start'])
            datetime_stop  = self.strip_time(program['datum_end'])
            if (datetime_start <= datetime_prog and datetime_prog <= datetime_stop):
                return program
        raise Exception('No program found')

    def json_write_file(self, data):
        f = open(self.cache_filename, 'w')
        f.write(data)
        f.close()

    def json_read_file(self):
        try:
            f = open(self.cache_filename, 'r')
            json_data = f.read()
            f.close()
            self.data = json.loads(json_data)
            self.get_current_program("1")        # check the date (will raise an error if the current program is not in it)
        except:
            return False    #return false on any Exception (file not found, no channel data, wrong date)
        return True

    def strip_time(self, date_string, format_str = "%Y-%m-%d %H:%M:%S"):
        try:
            t = datetime.strptime(date_string, format_str)
        except TypeError:
            t = datetime(*(time.strptime(date_string, format_str)[0:6]))
        return t
