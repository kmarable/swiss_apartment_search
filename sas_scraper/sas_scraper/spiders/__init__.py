#
# This has the base spider class with the basic logic:
# Scrape the start urls to get listings, repeat on all following results pages
# for each link to a listing, get the id, check against ids in our data file
# if we don't have it, download the page and save it for later processing.

import scrapy
from src.config import conf
import pandas as pd
import os
from datetime import date
from src.utilities import get_absolute_path
from src.utilities.htmlFile import htmlFile
from src.utilities.header import Header


class ApartmentSpider(scrapy.Spider):
    name = "Apartment"

    def __init__(self, category=None, max_downloads=500, *args, **kwargs):
        super(ApartmentSpider, self).__init__(*args, **kwargs)
        self.save_dir = get_absolute_path(conf['DEFAULT']['folder'])
        self.old_ids = self.getOldIDs()
        n_ids = len(self.old_ids)
        self.max_downloads = 1

        self.logger.debug('loading %i old ids' % n_ids)
        for id in self.old_ids:
            self.logger.debug('found old id %i' % id)

    def getOldIDs(self):
        old_data = pd.read_csv(self.getFilename())
        old_immobilier = old_data[old_data['host'] == self.getHost()]
        old_ids = [int(id) for id in old_immobilier['id']]
        return list(old_ids)

    def getFilename(self):
        file_path = get_absolute_path(conf['DEFAULT']['raw_file'])
        print('file path', file_path)
        if not os.path.exists(file_path):
            self.logger.warning('No raw file found')
            return []
        else:
            return file_path

    def start_requests(self):
        urls = self.getUrls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseMain)

    def parseMain(self, response):
        self.logger.info('parsing page %s' % response.url)

        listings = self.getListings(response)

        self.logger.info('found %i listings ' % len(listings))

        test, n_max = False, 200
        if not (self.pageIsLast(response) or test):
            next_page = self.getNextPage(response.url)
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parseMain)

        for i, l in enumerate(listings):
            id = self.getListingID(l)

            self.logger.debug('found id %i' % id)

            if (id in self.old_ids):
                continue  # go on to next link
            else:
                if i > n_max:
                    break
                link = self.getListingLink(l)

                self.logger.debug('sending request for %s' % link)

                full_link = response.urljoin(link)

                self.logger.debug('next list page is %s' % type(full_link))
                request = scrapy.Request(full_link, callback=self.savePage, encoding='utf-8')
                request.meta['id'] = id
                yield request

    def savePage(self, response):
        id = response.meta['id']  # get page id from the request sent in parseMain
        file_name = self.getListingFileName(id)
        save_file = htmlFile(file_name)
        newHeader = Header(response.url, id, self.getHost())
        save_file.write(response.text, newHeader)

        self.logger.debug('in savePage %s' % save_file.path)
        self.logger.debug('Saved file %s' % file_name)

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
        self.logger.debug('Saved file %s' % filename)
