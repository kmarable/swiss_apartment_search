from src.parser import ListingParser
import re
import string
import pandas as pd
import numpy as np
from src.utilities import make_case_insensitive
import config
import html
from datetime import datetime

class ImmoscoutListing(Listing):
    listings_folder = 'data\\immoscout_pages'
    test_file_path = 'test\\parsing_tests\\immoscout_gets.yaml'

    def __init__(response):
        self.response = response
        self.text = self._getText()

    def _getText(self):
        test_text = (response.body).decode("utf-8")
        return html.unescape(test_text)

    def getLoyerBrut(self):
        loyer_line = re.findall('Loyer brut \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', self.text)
        return self._getFirstInt(loyer_line)

    def getLoyerNet(self):
        assets = self.getText(response)
        loyer_line = re.findall('Loyer net \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', self.text)
        return self._getFirstInt(loyer_line)

    def getCharges(self):
        loyer_line = re.findall('Charges \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', self.text)
        return self._getFirstInt(loyer_line)

    def getAvailability(self):
        availabilities = re.findall( 'Disponibilité</td><td class=[^>]+>([0-9]{2}.[0-9]{2}.[0-9]{4})</td>', self.text)
        return self.getFirstDate(availabilities)

    def getConstructionYear(self):
        c_pattern = 'Année de construction</td><td class=[^>]+> ([0-9]+)'
        years = re.findall(c_pattern, self.text)
        return self._getSmallestInt(years)

    def getFloor(self):
        pattern = 'Étage</td><td class=[^>]*>([0-9]+). étage</td>'
        return self.getFirstInt(pattern, self.text)

    def getListingSpace(self, response):
        pattern = 'Surface habitable</td><td class=[^>]*>([0-9]+) m²</td>'
        return self.getFirstInt(pattern, self.text)

    def getAddress(self):
        address_pat = '>Emplacement</h2><p class=[^>]*>([a-zA-Z 0-9]+)<br/>([0-9]{4})<!-- --> <!-- -->([a-zA-Z]+) VD<!-- -->, VD</p>'
        rough_address = re.findall(address_pat, self.text)
        print ('ROUGH', rough_address)

        address_dict = {}

        if len(rough_address) == 0:
            return self._getDefaultAddress()
        else:
            address_dict['Street'] = address_dict = dict(zip(['Street', 'Zip', 'City'],
                                    [rough_address[0][0], rough_address[0][1],rough_address[0][2]]))
        return(address_dict)

    def getLatLong(self):
        latlong = re.findall('\"latitude\":([0-9.]+),\"longitude\":([0-9.]+)', self.text)
        return self._getFirstLatLong(latlong)

    def getDescription(self):
        pattern = 'Description</h2><div class=[^>]*>([^<]*)</div>'
        return self._getFirstString(pattern, self.text)

    def getReference(self, response):
        pattern = 'Référence</td><td class=[^>]*>([0-9.]+)</td>'
        return self._getFirstString(pattern, self.text)

    def getAnnouncer(self, response):
        pattern = 'Annonceur</h2><p class=[^>]*><span>([^<]*)<br/>'
        return self.getFirstString(pattern, self.text)
