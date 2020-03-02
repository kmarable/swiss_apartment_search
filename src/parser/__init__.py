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

# common helper functions

    def _getFirstInt(self, matches):
        if len(matches) > 0:
            return util.extract_french_number(matches[0])
        else:
            return -1

    def _getSmallestInst(self, matches):
        if len(matches) > 0:
            return (min([int(y) for y in years]))
        else:
            return self._getFirstInt(matches)

    def _getFirstString(self, matches):
        if len(matches) > 0:
            return matches[0]
        else:
            return ''

    def _getDefaultAddress(self):
        address_dict = dict(zip(['Street', 'Zip', 'City'],
                                ['', -1, '']))
        return address_dict

    def _getFirstLatLong(self, matches):
        if len(latlong) == 0:
            return {'Latitude': -1, 'Longitude': -1}
        else:
            return {'Latitude': float(latlong[0][0]),
                    'Longitude': float(latlong[0][1])}


    def _getFirstDate(self, matches):
        if len(matches) > 0:
            available_date = datetime.strptime( matches[0], '%d.%m.%Y')
            return available_date
        else:
            return datetime(0,0,0,0,0,0)

    def _loadRoomBasepatterns(self):
        with open('src\\parser\\rooms.yaml', encoding='utf8') as file:
            rooms = yaml.load(file, Loader=yaml.FullLoader)
            return(rooms)

    def _loadRoomColumns(self):
        rooms = self.load_room_basepatterns()
        room_columns = [r.split('|')[0] for r in rooms]
        return room_columns

# functions that return fields, all should be defined in inheriting classes
# here defined as finding no data and returning appropriate default for expected data type

    def getAvailability(self):
        matches =[]
        return self._getFirstDate(matches)

    def getConstructionYear(self):
        matches =[]
        return self._getFirstInt(matches)

    def getFloor(self):
        matches =[]
        return self._getFirstInt(matches)

    def getLoyerNet(self):
        matches =[]
        return self._getFirstInt(matches)

    def getCharges(self):
        matches =[]
        return self._getFirstInt(matches)

    def getLoyerBrut(self):
        matches =[]
        return self._getFirstInt(matches)

    def getListingSpace(self):
        matches =[]
        return self._getFirstInt(matches)

    def getDescription(self):
        matches =[]
        return self._getFirstString(matches)

    def getAddress(self):
        matches = []
        return self._getAddressString(matches)

    def getLatLong(self):
        return {'Latitude': -1, 'Longitude': -1}

    def getRooms(self):
        rooms = self._loadRoomColumns()
        return dict(zip(rooms), len(rooms)*[0])

    def getReference(self):
        matches =[]
        return self._getFirstString(matches)

    def getAnnouncer(self):
        matches =[]
        return self._getFirstString(matches)

    def getHost():
        matches =[]
        return self._getFirstString(matches)

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
