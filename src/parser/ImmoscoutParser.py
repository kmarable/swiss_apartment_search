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

    def getText(self, response):
        test_text = (response.body).decode("utf-8")
        return html.unescape(test_text)

    def getLoyerBrut(self, response):
        assets = self.getText(response)
        loyer_line = re.findall('Loyer brut \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getLoyerNet(self, response):
        assets = self.getText(response)
        loyer_line = re.findall('Loyer net \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getCharges(self, response):
        assets = self.getText(response)
        loyer_line = re.findall('Charges \(mois\)</td><td class=[^>]*>CHF ([^<]*).—</td>', assets)
        return extract_french_number(loyer_line)

    def getAvailability(self, response):
        assets = self.getText(response)
        # To do : convert to datetime
        availabilities = re.findall( 'Disponibilité</td><td class=[^>]+>([0-9]{2}.[0-9]{2}.[0-9]{4})</td>', assets)
        if len(availabilities) > 0:
            available_date = datetime.strptime( availabilities[0], '%d.%m.%Y')
            return available_date
        else:
            return ''

    def getConstructionYear(self, response):
        assets = self.getText(response)
        c_pattern = 'Année de construction</td><td class=[^>]+> ([0-9]+)'
        years = re.findall(c_pattern, assets)
        if len(years) > 0:
            return (min([int(y) for y in years]))
        else:
            return -1

    def getFloor(self, response):
        pattern = 'Étage</td><td class=[^>]*>([0-9]+). étage</td>'
        return self.getFirstIntMatchingPattern(pattern, response)

    def getListingSpace(self, response):
        pattern = 'Surface habitable</td><td class=[^>]*>([0-9]+) m²</td>'
        return self.getFirstIntMatchingPattern(pattern, response)

    def getAddress(self, response):
        assets = self.getText(response)
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
        assets = self.getText(response)
        latlong = re.findall('\"latitude\":([0-9.]+),\"longitude\":([0-9.]+)', assets)
        if len(latlong) == 0:
            return {'Latitude': -1, 'Longitude': -1}
        else:
            return {'Latitude': float(latlong[0][0]),
                    'Longitude': float(latlong[0][1])}

    def getDescription(self, response):
        pattern = 'Description</h2><div class=[^>]*>([^<]*)</div>'
        return self.getFirstStringMatchingPattern(pattern, response)


    def getReference(self, response):
        pattern = 'Référence</td><td class=[^>]*>([0-9.]+)</td>'
        return self.getFirstStringMatchingPattern(pattern, response)

    def getAnnouncer(self, response):
        pattern = 'Annonceur</h2><p class=[^>]*><span>([^<]*)<br/>'
        return self.getFirstStringMatchingPattern(pattern, response)

    def getFirstStringMatchingPattern(self, pattern, response):
        text = self.getText(response)
        matches = re.findall(pattern, text)
        print('matches', matches)
        if len(matches) > 0:
            return matches[0]
        else:
            return ''

    def getFirstIntMatchingPattern(self, pattern, response):
        text = self.getText(response)
        matches = re.findall(pattern, text)
        if len(matches) > 0:
            return extract_french_number(matches)
        else:
            return -1
