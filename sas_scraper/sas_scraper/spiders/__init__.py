#
# This has the base spider class with the basic logic:
# Scrape the start urls to get listings, repeat on all following results pages
# for each link to a listing, get the id, check against ids in our data file
# if we don't have it, download the page and save it for later processing.

import scrapy
import logging
from scrapy.utils.log import configure_logging
from src.config import conf
import pandas as pd
import os
from datetime import date
from src.utilities.htmlFile import htmlFile
from src.utilities.header import Header


class ApartmentSpider(scrapy.Spider):
    name = "Apartment"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='ApartmentSpiderLog.txt',
        format='%(levelname)s: %(message)s',
        level=logging.DEBUG
    )

    def __init__(self, category=None, *args, **kwargs):
        super(ApartmentSpider, self).__init__(*args, **kwargs)
        self.save_dir = conf['DEFAULT']['folder']
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
            old_immobilier = old_data[old_data['host'] == self.getHost()]
            old_ids = [int(id) for id in old_immobilier['id']]
            return list(old_ids)

    def start_requests(self):
        urls = self.getUrls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseMain)

    def parseMain(self, response):
        self.log('parsing page %s' % response.url)
        listings = self.getListings(response)
        self.log('found %i listings ' % len(listings))

        if not self.pageIsLast(response):
            next_page = self.getNextPage(response.url)
            self.log('next page is %s' % type(next_page))
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parseMain)

        n_max = 50 # maximum downloads per page, used during testing
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
                self.log('next list page is %s' % type(full_link))
                request = scrapy.Request(full_link, callback=self.savePage)
                request.meta['id'] = id
                yield request

    def savePage(self, response):
        id = response.meta['id']
        file_name = self.getListingFileName(id)
        save_file = htmlFile(file_name)
        self.log('in savePage %s' % save_file.path)
        newHeader = Header(response.url, id, self.getHost())
        save_file.write(response.text, newHeader)
        self.log('Saved file %s' % file_name)

    def getListingFileName(self, id):
        today = str(date.today())

        file_name = os.path.join(self.save_dir,
                                 today + '_' + str(id) + '.html')
        return file_name

# defined in child classes
    def getHost(self):
        raise NotImplementedError

    def getUrls(self):
        pass

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

# mostly for testing
    def save_main_page(self, response):
        filename = os.path.join(self.save_dir, 'test_page.html')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
