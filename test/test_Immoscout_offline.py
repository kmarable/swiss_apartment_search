import unittest
from sas_scraper.sas_scraper.spiders.ImmoscoutSpider import ImmoscoutSpider
import sys
import os
from src.utilities import response_from_file
from datetime import date
from scrapy.selector import Selector


class TestImmoscoutSpider(unittest.TestCase):
    def setUp(self):
        self.spider = ImmoscoutSpider()
        self.test_file_name = "sas_scraper\\test_immoscout.html"
        self.html = response_from_file(self.test_file_name)
        self.test_listing = self.spider.getListings(self.html)[0]

    def test_getListings(self):
        listings = self.spider.getListings(self.html)
        print(listings[0])
        self.assertEqual(len(listings), 24)

    def test_getListingLink(self):
        expected = "https://www.immoscout24.ch/fr/d/appartement-louer-lausanne/5892534?s=1&t=1&l=2023&ct=767&ci=1&pn=1"
        result = self.spider.getListingLink(self.test_listing)
        print('RESULT', result)
        self.assertEqual(expected, result)

    def test_getListingID(self):
        expected = 5892534
        result = self.spider.getListingID(self.test_listing)
        print('listing id result', result)
        self.assertEqual(expected, result)

    def test_getListingFileName(self):
        today = str(date.today())
        expected = "data\\saved_pages\\" + today + '_1.html'
        result = self.spider.getListingFileName(1)
        print('EXP', expected)
        self.assertEqual(expected, result)

    def test_getNextPage(self):
        result = self.spider.getNextPage('https://www.immoscout24.ch/fr/immobilier/louer/lieu-lausanne?pn=1')
        expected = 'https://www.immoscout24.ch/fr/immobilier/louer/lieu-lausanne?pn=2'
        self.assertEqual(result, expected)

    def test_pageIsLast(self):
        self.assertFalse(self.spider.pageIsLast(self.html))
