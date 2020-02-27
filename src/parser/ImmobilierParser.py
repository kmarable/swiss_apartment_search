from src.parser import ListingParser
import re
import string
import pandas as pd
import numpy as np
from src.utilities import make_case_insensitive


class ImmobilierParser(ListingParser):
    listings_folder = 'data\\immobilier_pages'

    def getListingAssets(self, response):
        assets = response.css('div.im__assets__table').get()
        if assets is None:
            return ''
        else:
            return assets

    def getAvailability(self, response):
        assets = self.getListingAssets(response)
        # To do : convert to datetime
        availabilities = re.findall(r'Disponible dès\s*(.*\S)[\s\t]*', assets)
        if len(availabilities) > 0:
            return availabilities[0]
        else:
            return 'No info'

    def getConstructionYear(self, response):
        assets = self.getListingAssets(response)
        c_pattern = r'onstruit en\s*([0-9]*)[\s\t]*'
        years = re.findall(c_pattern, assets)
        if len(years) > 0:
            return (min([int(y) for y in years]))
        else:
            return -1

    def getFloor(self, response):
        assets = self.getListingAssets(response)
        if re.search(r'Rez-de-chaussée', assets):
            return 0
        floors = re.findall(r'([2-9])ème étage', assets)
        floors.extend(re.findall(r'(1)er étage', assets))
        if len(floors):
            return int(floors[0])
        else:
            return -1

    def getLoyerNet(self, response):
        assets = self.getListingAssets(response)
        loyer_line = re.findall('Loyer : CHF [0-9\']*.-/mois', assets)
        return extract_french_number(loyer_line)

    def getCharges(self, response):
        assets = self.getListingAssets(response)
        charges_line = re.findall('Charges : CHF [0-9\']*', assets)
        return extract_french_number(charges_line)

    def getListingSpace(self, response):
        assets = self.getListingAssets(response)
        space = re.findall(r'([0-9]+)\sm<sup', assets)

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
        assets = self.getListingAssets(response)
        address_pat = 'big\">\s*([\w\s-]+)(<br>)*([\w\s-]+)<br>\s*<a'
        #'big\">\s*([\w\s]*)(<br>)*([\w\s-]*)<br>\s<a'
        rough_address = re.findall(address_pat, assets)

        address_dict = {}

        if len(rough_address) == 0:
            print('NO ADDRESS FOUND')
            address_dict = dict(zip(['Street', 'Zip', 'City'],
                                    ['', '', -1, '']))
            return address_dict

        address = rough_address[0]

        if len(address) > 1:
            address_dict['Street'] = address[0]
            self.addZipAndCitytoDict(address_dict, address[2])
        else:
            self.addZipAndCitytoDict(address_dict, address[0])
            if address_dict['Zip'] == -1:
                address_dict['Street'] = address[0]
            else:
                address_dict['Street'] = ''
        return(address_dict)

    def getLatLong(self, response):
        assets = self.getListingAssets(response)
        latlong = re.findall(r'query=([0-9.]+),([0-9.]+)"', assets)
        if len(latlong) == 0:
            return {'Latitude': -1, 'Longitude': -1}
        else:
            return {'Latitude': float(latlong[0][0]),
                    'Longitude': float(latlong[0][1])}

    def getDescription(self, response):
        postContent = response.css('div.im__postContent__body p').get()
        if postContent is None:
            return ''
        else:
            return(postContent)

    def getRooms(self, response):
        test = self.getDescription(response)
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

    def getHost(self):
        return 'Immobilier'


def extract_french_number(num_string_list):
    if len(num_string_list) == 0:
        return -1
    defrenched = ''.join([p.replace('\'', '') for p in num_string_list[0]])
    price = re.findall('[0-9]+', defrenched)[0]
    return int(price)
