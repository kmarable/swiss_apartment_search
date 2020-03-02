from os import listdir
from os.path import join
import pandas as pd
import yaml
import re
from datetime import datetime
import src.utilities as util
from src.utilities.htmlFile import htmlFile
from src.utilities.dataFile import DataFile

class Listing():
    def __init__(response):
        self.response = response


    def getFirstInt(self, matches):
        if len(matches) > 0:
            return util.extract_french_number(matches)
        else:
            return -1

    def getFirstString(self, matches):
        if len(matches) > 0:
            return matches[0]
        else:
            return ''

    def getFirstDate(self, matches):
        if len(matches) > 0:
            return datetime.strptime(matches[0])
        else:
            return datetime(0,0,0,0,0,0)

class ListingParser():
    listings_folder = ''

    def __init__(self):
        if self.listings_folder == '':
            raise Exception
        self.files = [join(self.listings_folder, f) for f in listdir(self.listings_folder)]

    def extractAll(self):
        htmlFiles = [htmlFile(f) for f in self.files]
        headerData = self.parseAllHeaders(htmlFiles)
        responses = [f.getResponse() for f in htmlFiles]
        fileData = self.parseAllFiles(responses)
        new_data = headerData.join(fileData)
        self.write_file(new_data)

    def parseAllHeaders(self, htmlFiles):
        headers = [f.read()[0] for f in htmlFiles]
        new_data = dictListToDataFrame(headers)
        return new_data

    def parseAllFiles(self, rs):
        new_data = pd.DataFrame()
        new_data['Availability'] = [self.getAvailability(r) for r in rs]
        new_data['Year'] = [self.getConstructionYear(r) for r in rs]
        new_data['Floor'] = [self.getFloor(r) for r in rs]
        new_data['LoyerNet'] = [self.getLoyerNet(r) for r in rs]
        new_data['Charges'] = [self.getCharges(r) for r in rs]
        new_data['Space'] = [self.getListingSpace(r) for r in rs]
        address_df = dictListToDataFrame([self.getAddress(r) for r in rs])
        new_data = new_data.join(address_df)
        latlong_df = dictListToDataFrame([self.getLatLong(r) for r in rs])
        new_data = new_data.join(latlong_df)
        rooms_df = dictListToDataFrame([self.getRooms(r) for r in rs])
        new_data = new_data.join(rooms_df)
        new_data['Description'] = [self.getDescription(r) for r in rs]
        return new_data

    def write_file(self, new_data):
        df_file = DataFile()
        df_file.updateFile(new_data)

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

    def load_rooms(self):
        with open('src\\parser\\rooms.yaml', encoding='utf8') as file:
            rooms = yaml.load(file, Loader=yaml.FullLoader)
            return(rooms)

    def getAvailability(self, r):
        pass

    def getYear(self, r):
        pass

    def getFloor(self, r):
        pass

    def getAddress(self, r):
        pass

    def getLoyer(self, r):
        pass

    def getCharges(self, r):
        pass

    def getSpace(self, r):
        pass

    def getReference(self, r):
        pass

    def getPoster(self, r):
        pass
