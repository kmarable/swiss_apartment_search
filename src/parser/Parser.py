import os
import pandas as pd
from src.config import conf
import src.utilities as util
from src.utilities.htmlFile import htmlFile
from src.parser.listing import Listing
from src.parser.listing.ImmobilierListing import ImmobilierListing
from src.parser.listing.ImmoscoutListing import ImmoscoutListing


class Parser():

    def __init__(self):
        self.listings_folder = util.get_absolute_path(conf['DEFAULT']['folder'])
        lf = os.path.normpath(self.listings_folder)
        self.files = [os.path.join(lf, f) for f in os.listdir(lf)]

    def extractAll(self):
        htmlFiles = [htmlFile(f) for f in self.files]
        print('start parsing')
        headerData = self.parseAllHeaders(htmlFiles)
        print('got headers')
        listings = self.getAllListings(htmlFiles, headerData)
        fileData = self.parseAllListings(listings)
        new_data = headerData.join(fileData)
        save_file = os.path.normpath(conf['DEFAULT']['raw_file'])
        new_data.to_csv(save_file)

    def parseAllHeaders(self, htmlFiles):
        headers = [f.read()['HEADER'].__dict__ for f in htmlFiles]
        new_data = util.dictListToDataFrame(headers)
        print(len(headers))
        return new_data

    def parseAllListings(self, listings):
        new_data = pd.DataFrame()

        methods = util.get_get_functions(Listing)
        for m in methods:
            print(m)
            new_field = [getattr(l, m)() for l in listings]
            if isinstance(new_field[0], dict):
                new_df = util.dictListToDataFrame(new_field)
                new_data = new_df.join(new_data, how='outer')
            else:
                field_name = m.replace('get', '')
                new_data[field_name] = new_field
        return new_data

    def getAllListings(self, htmlFiles, headerData):
        hosts = headerData['host']
        rs = [f.getResponse() for f in htmlFiles]
        fileParsers = [self.getListing(h, hr) for h, hr in zip(rs, hosts)]
        print('parsers loaded', len(fileParsers))
        return fileParsers

    def getListing(self, response, host):
        factory_dict = {
            "Immobilier": ImmobilierListing(response),
            "Immoscout": ImmoscoutListing(response)
        }
        return factory_dict[host]
