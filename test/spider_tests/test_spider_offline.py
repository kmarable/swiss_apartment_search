import unittest
from sas_scraper.sas_scraper.spiders.ImmobilierSpider import ImmobilierSpider
import sys
import os
from src.utilities import response_from_file
from datetime import date
from scrapy.selector import Selector


class TestImmobilierSpider(unittest.TestCase):
    def setUp(self):
        self.spider = ImmobilierSpider()
        self.test_file_name = "sas_scraper\\test-immobilier.html"
        self.html = response_from_file(self.test_file_name)
        self.test_listing = self.html.css('div.filter-item-container')[0]

    def test_getOldIDs(self):
        old_ids = self.spider.getOldIDs()
        self.assertGreater(len(old_ids), 0)

    def test_getListings(self):
        listings = self.spider.getListings(self.html)
        self.assertEqual(len(listings), 24)

    def test_getListingLink(self):
        expected = '/fr/louer/place-parc/neuchatel/st-aubin-sauges/naef-immobilier-neuchatel-115/place-ouverte-380720'
        result = self.spider.getListingLink(self.test_listing)
        self.assertEqual(expected, result)

    def test_getListingID(self):
        expected = 380720
        result = self.spider.getListingID(self.test_listing)
        self.assertEqual(expected, result)

    def test_getListingFileName(self):
        today = str(date.today())
        expected = "data\\saved_pages\\" + today + '_1.html'
        result = self.spider.getListingFileName(1)
        print('EXP', expected)
        self.assertEqual(expected, result)

    def test_getNextPage(self):
        result = self.spider.getNextPage('https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/renens/page-1?t=rent&c=1;2&p=c12292&nb=false')
        expected = 'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/renens/page-2?t=rent&c=1;2&p=c12292&nb=false'
        self.assertEqual(result, expected)

    def test_pageIsLast(self):
        isLast = Selector(text='<div class="items-result-count">162-163 / 163 biens</div>')
        isNotLast = Selector(text='<div class="items-result-count">1-20 / 163 biens</div>')

        self.assertTrue(self.spider.pageIsLast(isLast))
        self.assertFalse(self.spider.pageIsLast(isNotLast))
