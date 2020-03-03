import os
import re
import pandas as pd
from datetime import date
from sas_scraper.sas_scraper.spiders import ApartmentSpider


class ImmobilierSpider(ApartmentSpider):
    name = "Immobilier"

    def getHost(self):
        return 'Immobilier'

    def getUrls(self):
        urls = [
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/renens/page-1?t=rent&c=1;2&p=c12292&nb=false',
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/lausanne/page-1?t=rent&c=1;2&p=c11115&nb=false&gr=1',
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/ecublens/page-1?t=rent&c=1;2&p=c10033&nb=false&gr=1', 'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/prilly/page-1?t=rent&c=1;2&p=c12211&nb=false&gr=1'
        ]
        return urls

    def getListings(self, response):
        return response.css('div.filter-item-container')

    def pageIsLast(self, response):
        items_on_page = response.css("div.items-result-count").get()
        results = re.search('([0-9]+) / ([0-9]+)', items_on_page)
        if results.group(1) == results.group(2):
            return True
        else:
            return False

    def getNextPage(self, url):
        result = re.findall('(.*page-)([0-9]+)(\?.*)', url)
        if len(result) > 0:
            address_components = result[0]
            page_num = address_components[1]
            new_page_num = int(page_num) + 1
            new_address = address_components[0] + str(new_page_num) + address_components[2]
            return(new_address)
        else:
            print('bad address format')
            return None

    def getListingLink(self, listing):
        link = listing.css("a[id^='link-result-item']::attr(href)").get()
        return link

    def getListingID(self, listing):
        id = listing.css("a[id^='link-result-item']::attr(id)").get()
        if id is None:
            return -1
        id_num = re.findall('[0-9]+', id)
        if len(id_num) > 0:
            return int(id_num[0])
        else:
            return -1
