from src.parser import ListingParser
import re
import string
import pandas as pd
import numpy as np
from src.utilities import make_case_insensitive, extract_french_number
import config
import html
from datetime import datetime

class ImmoscoutParser(ListingParser):
    listings_folder = 'data\\immoscout_pages'

    def getLoyerBrut(self, response):
        assets = html.unescape(response.text)
        loyer_line = re.findall('Loyer brut \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getLoyerNet(self, response):
        assets = html.unescape(response.text)
        loyer_line = re.findall('Loyer net \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getCharges(self, response):
        assets = html.unescape(response.text)
        loyer_line = re.findall('Charges \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getAvailability(self, response):
        assets = html.unescape(response.text)
        # To do : convert to datetime
        availabilities = re.findall( 'Disponibilité</td><td class=[^>]+>([0-9]{2}.[0-9]{2}.[0-9]{4})</td>', assets)
        if len(availabilities) > 0:
            available_date = datetime.strptime( availabilities[0], '%d.%m.%Y')
            return available_date
        else:
            return 'No info'

    def getConstructionYear(self, response):
        assets = html.unescape(response.text)
        c_pattern = 'Année de construction</td><td class=[^>]+> ([0-9]+)'
        years = re.findall(c_pattern, assets)
        if len(years) > 0:
            return (min([int(y) for y in years]))
        else:
            return -1

    def getFloor(self, response):
        assets = html.unescape(response.text)
        floors = re.findall('Étage</td><td class=[^>]*>([0-9]+). étage</td>', assets)
        print(floors)
        if len(floors):
            return int(floors[0])
        else:
            return -1

    def getListingSpace(self, response):
        assets = html.unescape(response.text)
        space = re.findall('Surface habitable</td><td class=[^>]*>([0-9]+) m²</td>', assets)

        if len(space) > 0:
            return int(space[0])
        else:
            return -1

    def addZipAndCitytoDict(self, address_dict, string):
        city_pat = '(Prilly|Renens|Ecublens|Lausanne)'
        zip_pat = '([0-9]{4})'
        zip_city = re.findall(zip_pat + '\s' + city_pat, string)
        if len(zip_city) == 0:
            address_dict['Zip'] = -1
            address_dict['City'] = ''
        else:
            address_dict['Zip'] = zip_city[0][0]
            address_dict['City'] = zip_city[0][1]

    def getAddress(self, response):
        assets = html.unescape(response.text)
        address_pat = '>Emplacement</h2><p class=[^>]*>([a-zA-Z 0-9]+)<br/>([0-9]{4})<!-- --> <!-- -->([a-zA-Z]+) VD<!-- -->, VD</p>'
        #'>Emplacement</h2><p class=[^>]*>([.]+)<br/>([0-9]{4})<!-- --> <!-- -->([a-zA-Z]) VD<!-- -->, VD</p>'
        #'big\">\s*([\w\s]*)(<br>)*([\w\s-]*)<br>\s<a'
        rough_address = re.findall(address_pat, assets)
        print ('ROUGH', rough_address)

        address_dict = {}

        if len(rough_address) == 0:
            print('NO ADDRESS FOUND')
            address_dict = dict(zip(['Street', 'Zip', 'City'],
                                    ['',  -1, '']))
        else:
            address_dict['Street'] = address_dict = dict(zip(['Street', 'Zip', 'City'],
                                    [rough_address[0][0], rough_address[0][1],rough_address[0][2]]))
        return(address_dict)

    def getLatLong(self, response):
        assets = html.unescape(response.text)
        latlong = re.findall('\"latitude\":([0-9.]+),\"longitude\":([0-9.]+)', assets)
        if len(latlong) == 0:
            return {'Latitude': -1, 'Longitude': -1}
        else:
            return {'Latitude': float(latlong[0][0]),
                    'Longitude': float(latlong[0][1])}

    def getDescription(self, response):
        assets = html.unescape(response.text)
        postContent = re.findall('Description</h2><div class=[^>]*>([^>]*)</div>', assets )
        if postContent is []:
            return ''
        else:
            return(postContent[0])

    def getRooms(self, response):
        test = self.getDescription(response)
        print('desc', test)
        quantity_dict = {'': 1,  'un': 1, 'une': 1, 'deux': 2}

        def quantity_to_int(q):
            if q in quantity_dict:
                return quantity_dict[q]
            else:
                return int(q)

        def get_quantity_pattern():
            keys = quantity_dict.keys()
            quantities_from_dict = ''.join(['|' + k for k in keys if k != ''])
            quantities = '([0-9]*' + quantities_from_dict + ')'
            return(quantities)

        rooms = self.load_rooms()
        room_columns = [r.split('|')[0] for r in rooms]
        rooms_patt = ['(' + make_case_insensitive(r) + ')' for r in rooms]

        rooms_in_ad = {}
        for p, col in zip(rooms_patt, room_columns):
            re_str = get_quantity_pattern() + '\s*' + p
            result = re.findall(re_str, test)
            numbers_mentioned = [quantity_to_int(r[0]) for r in result]
            rooms_in_ad[col] = sum(numbers_mentioned)

        return(rooms_in_ad)
