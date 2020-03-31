import yaml
import re
from datetime import datetime
import dateparser
import src.utilities as util


class Listing():
    def __init__(self, response):
        self.section = 'DEFAULT'
        self.setAttributes(response)

    def setAttributes(self, response):
        self.response = response

# common helper functions

    def _getFirstInt(self, matches):
        if len(matches) > 0:
            return util.extract_french_number(matches[0])
        else:
            return -1

    def _getSmallestInt(self, matches):
        if len(matches) > 0:
            return (min([int(m) for m in matches]))
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
        if len(matches) == 0:
            return {'Latitude': -1, 'Longitude': -1}
        else:
            return {'Latitude': float(matches[0][0]),
                    'Longitude': float(matches[0][1])}

    def _getFirstDate(self, matches):
        if len(matches) > 0:
            settings = {'DATE_ORDER': 'DMY', 'PREFER_DAY_OF_MONTH': 'first'}
            available_date = dateparser.parse(matches[0], settings=settings)
            if available_date is not None:
                return available_date
        return datetime(1970, 1, 1)

    def _loadRoomBasePatterns(self):
        with open('src\\parser\\listing\\rooms.yaml', encoding='utf8') as file:
            rooms = yaml.load(file, Loader=yaml.FullLoader)
            return(rooms)

    def _loadRoomColumns(self):
        rooms = self._loadRoomBasePatterns()
        room_columns = [r.split('|')[0] for r in rooms]
        return room_columns

# functions that return fields, all should be defined in inheriting classes
# here defined as finding no data then returning appropriate default for
# expected data type

    def getAvailability(self):
        matches = []
        return self._getFirstDate(matches)

    def getConstructionYear(self):
        matches = []
        return self._getFirstInt(matches)

    def getFloor(self):
        matches = []
        return self._getFirstInt(matches)

    def getLoyerNet(self):
        matches = []
        return self._getFirstInt(matches)

    def getCharges(self):
        matches = []
        return self._getFirstInt(matches)

    def getLoyerBrut(self):
        matches = []
        return self._getFirstInt(matches)

    def getListingSpace(self):
        matches = []
        return self._getFirstInt(matches)

    def getDescription(self):
        matches = []
        return self._getFirstString(matches)

    def getAddress(self):
        return self. _getDefaultAddress()

    def getLatLong(self):
        return {'Latitude': -1, 'Longitude': -1}

    def getReference(self):
        matches = []
        return self._getFirstString(matches)

    def getAnnouncer(self):
        matches = []
        return self._getFirstString(matches)

# Functions that return fields but are defined here
# because they should be # generic across websites

    def getRooms(self):
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

        rooms = self._loadRoomBasePatterns()
        rooms_patt = ['(' + util.make_case_insensitive(r) + ')' for r in rooms]
        rooms_in_ad = {}
        description = self.getDescription()

        for room_patt, room_col in zip(rooms_patt, self._loadRoomColumns()):
            room_quantity_pattern = get_quantity_pattern() + r'\s*' + room_patt
            result = re.findall(room_quantity_pattern, description)
            numbers_mentioned = [quantity_to_int(r[0]) for r in result]
            rooms_in_ad[room_col] = sum(numbers_mentioned)

        return(rooms_in_ad)
