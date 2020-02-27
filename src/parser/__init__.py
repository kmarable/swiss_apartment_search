from os import listdir
from os.path import join
import pandas as pd
import yaml
from src.utilities import dictListToDataFrame
from src.utilities.htmlFile import htmlFile
from src.utilities.dataFile import DataFile


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

    def getAvailability(self, r):
        pass

    def getYear(self, r):
        pass

    def getFloor(self, r):
        pass

    def getAddress(self, r):
        pass

    def getRooms(self, r):
        pass

    def getLoyer(self, r):
        pass

    def getCharges(self, r):
        pass

    def getSpace(self, r):
        pass

    def load_rooms(self):
        with open('src\\parser\\rooms.yaml', encoding='utf8') as file:
            rooms = yaml.load(file, Loader=yaml.FullLoader)
            return(rooms)
