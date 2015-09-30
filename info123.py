#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import datetime
import pprint       # For debugging

def log(s):
    print(s)

class info123:
    def __init__(self, channelstring = "1,2,3"):
        self.data = []
        self.json_url = "http://www.tvgids.nl/json/lists/programs.php?channels=" + channelstring
        self.update()

    def update(self):
        response = urlopen(self.json_url)     #TODO create something with a timeout
        self.data = json.loads(response.read())

    def get_current_program(self, channel):
        return self.get_program(datetime.datetime.now(), channel)

    def get_program(self, datetime_prog, channel):
        # format:
        # u'datum_end': u'2015-10-01 00:15:00',
        # u'datum_start': u'2015-09-30 23:55:00',
        # u'db_id': u'19081949',
        # u'genre': u'Nieuws/actualiteiten',
        # u'kijkwijzer': u'',
        # u'soort': u'Nieuwsbulletin',
        # u'titel': u'Journaal'}]

        channel_info = self.data[channel]       #TODO check if channel exists
        for program in channel_info:
            datetime_start = datetime.datetime.strptime(program['datum_start'], "%Y-%m-%d %H:%M:%S")
            datetime_stop  = datetime.datetime.strptime(program['datum_end'],   "%Y-%m-%d %H:%M:%S")
            if (datetime_start <= datetime_prog and datetime_prog <= datetime_stop):
                return program
        raise Exception('program', 'not found!')



    def log_data(self):
        pp = pprint.PrettyPrinter(indent=4)
        log(pp.pprint(self.data['1']))

tv = info123()
# tv.log_data()
prog = tv.get_current_program("1")
print("nu op nederland 1: " + prog['titel'] + "\nvan: " + prog['datum_start'] + "\ntot: " + prog['datum_end'])
