# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import logging
from scrapy.utils.log import configure_logging
from src.config import conf
import pandas as pd
import os
from datetime import date
from src.utilities.htmlFile import htmlFile


class ApartmentSpider(scrapy.Spider):
    name = "Apartment"
    filename_root = "data\\saved_pages\\"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='ApartmentSpiderLog.txt',
        format='%(levelname)s: %(message)s',
        level=logging.DEBUG
    )

    def __init__(self, category=None, *args, **kwargs):
        super(ApartmentSpider, self).__init__(*args, **kwargs)

        self.old_ids = self.getOldIDs()
        n_ids = len(self.old_ids)
        self.log('loading %i old ids' % n_ids)
        for id in self.old_ids:
            self.log('found old id %i' % id)

    def getOldIDs(self):
        file_name = conf['DEFAULT']['raw_file']
        if not os.path.exists(file_name):
            return []
        else:
            old_data = pd.read_csv(file_name)
            old_immobilier = old_data[old_data['host'] == self.getSite() + '\n']
            old_ids = [int(id) for id in old_immobilier['id']]
            return list(old_ids)

    def getSite(self):
        pass

    def start_requests(self):
        urls = self.getUrls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseMain)

    def getUrls(self):
        pass

    def parseMain(self, response):
        self.log('parsing page ')
        listings = self.getListings(response)
        self.log('found %i listings ' % len(listings))

        if not self.pageIsLast(response):
            next_page = self.getNextPage(response.url)
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parseMain)

        n_max = 2
        i = 0
        for l in listings:
            id = self.getListingID(l)
            self.log('found id %i' % id)
            if i > n_max:
                return
            elif (id in self.old_ids):
                continue  # go on to next link
            else:
                i = i+1
                link = self.getListingLink(l)
                self.log('sending request for %s' % link)
                full_link = response.urljoin(link)
                request = scrapy.Request(full_link, callback=self.savePage)
                request.meta['id'] = id
                yield request

    def getListings(self, response):
        pass

    def pageIsLast(self, response):
        pass

    def getNextPage(self, url):
        pass

    def getListingLink(self):
        pass

    def getListingID(self):
        pass

    def savePage(self, response):
        id = response.meta['id']
        file_name = self.getListingFileName(id)
        save_file = htmlFile(file_name)
        self.log('in savePage %s' % save_file.path)
        # make header_dict
        header_dict = {}
        header_dict['link'] = response.url
        header_dict['id'] = id
        header_dict['host'] = self.getSite()
        header_dict['date'] = str(date.today())
        save_file.write(response.text, header_dict)
        self.log('Saved file %s' % file_name)

    def getListingFileName(self, id):
        today = str(date.today())

        file_name = os.path.join(ApartmentSpider.filename_root,
                                 today + '_' + str(id) + '.html')
        return file_name

    def save_main_page(self, response):
        filename = os.path.join(ApartmentSpider.filename_root, 'test_page.html')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
