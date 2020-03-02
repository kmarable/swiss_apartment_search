from src.parser import ListingParser
import re
import string
import pandas as pd
import numpy as np
from src.utilities import make_case_insensitive, extract_french_number

class ImmobilierListing(Listing):
    listings_folder = 'data\\immobilier_pages'
    test_file_path = 'test\\parsing_tests\\immobilier_gets.yaml'

    def __init__(response):
        self.response = response
        self.assets = self._getListingAssets()

    def _getListingAssets(self):
        assets = self.response.css('div.im__assets__table').get()
        if assets is None:
            return ''
        else:
            return assets

    def getAvailability(self):
        availabilities = re.findall(r'Disponible dès\s*(.*\S)[\s\t]*', self.assets)
        return self._getFirstDate(availabilities)

    def getConstructionYear(self):
        c_pattern = r'onstruit en\s*([0-9]*)[\s\t]*'
        years = re.findall(c_pattern, self.assets)
        return self._getFirstInt(years)

    def getFloor(self):
        if re.search(r'Rez-de-chaussée', self.assets):
            return 0
        floors = re.findall(r'([2-9])ème étage', self.assets)
        floors.extend(re.findall(r'(1)er étage', self.assets))
        return self._getFirstInt(floors)

    def getLoyerNet(self):
        loyer_line = re.findall('Loyer : CHF [0-9\']*.-/mois', self.assets)
        return self._getFirstInt(loyer_line)

    def getCharges(self):
        assets = self.getListingAssets(response)
        charges_line = re.findall('Charges : CHF [0-9\']*', self.assets)
        return self._getFirstInt(loyer_line)

    def getLoyerBrut(self):
        #no example found yet, but search just in case
        #will calculate from Net +Charges in postprocessing
        assets = self.getListingAssets(response)
        charges_line = re.findall('Brut : CHF [0-9\']*', self.assets)
        return self._getFirstInt(loyer_line)

    def getListingSpace(self):
        space = re.findall(r'([0-9]+)\sm<sup', self.assets)
        return self._getFirstInt(space)

    def getDescription(self):
        postContent = response.css('div.im__postContent__body p').get()
        if postContent is None:
            return ''
        else:
            return(postContent)

    def getAddress(self):

        def addZipAndCitytoDict(string):
            city_pat = '(Prilly|Renens|Ecublens|Lausanne)'
            zip_pat = '([0-9]{4})'
            zip_city = re.findall(zip_pat + '\s' + city_pat, string)
            if len(zip_city) == 0:
                address_dict['Zip'] = -1
                address_dict['City'] = ''
            else:
                address_dict['Zip'] = zip_city[0][0]
                address_dict['City'] = zip_city[0][1]

        def parseIncompleteAddress(address):
            addZipAndCitytoDict(address_dict, address)
            if address_dict['Zip'] == -1:
                address_dict['Street'] = address
            else:
                address_dict['Street'] = ''

        address_pat = 'big\">\s*([\w\s-]+)(<br>)*([\w\s-]+)<br>\s*<a'
        matches = re.findall(address_pat, self.assets)
        address = self._getFirstString(matches)

        address_dict = {}
        if len(address) == 0:
            address_dict= self._getDefaultAddress(address)
        elif len(address) == 1:
            parseIncompleteAddress(address_strings[0])
        else len(address) > 1:
            address_dict['Street'] = address[0]
            addZipAndCitytoDict(address_dict, address[2])

        return address__dict

    def getLatLong(self):
        latlong = re.findall(r'query=([0-9.]+),([0-9.]+)"', self.assets)
        return self._getFirstLatLong(latlong)

    def getRooms(self, response):
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
        rooms_patt = ['(' + make_case_insensitive(r) + ')' for r in rooms]
        rooms_in_ad = {}
        description = self.getDescription()

        for room_patt, room_col in zip(rooms_patt, self._load_room_columns()):
            room_quantity_pattern = get_quantity_pattern() + '\s*' + room_patt
            result = re.findall(room_quantity_pattern, description)
            numbers_mentioned = [quantity_to_int(r[0]) for r in result]
            rooms_in_ad[room_col] = sum(numbers_mentioned)

        return(rooms_in_ad)


    def getReference(self):
        reference = re.findall('rence\s*([0-9.]+)\s*</span>', self.assets)
        return self.getFirstSting(reference)

    def getAnnouncer(self, response):
        html_text =  (self.response.body).decode("utf-8")
        announcer = re.findall('<strong>([^<]+)</strong>', html_text)
        return self.getFirstSting(announcer)
