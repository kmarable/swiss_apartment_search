import unittest
from sas_scraper.sas_scraper.spiders.apartment_spider import *
import sys
import os
from test.utilities import fake_response_from_file

class TestImmobilierSpider(unittest.TestCase):
    def setUp(self):
        print(sys.path)
        self.spider = ImmobilierSpider()
        self.test_file_name = "..\\sas_scraper\\test-immobilier.html"
        self.html = fake_response_from_file(self.test_file_name)
        self.test_listing = self.html.css('div.filter-item-container')[0]

    def test_parse(self):
        print (self.spider.parseMain(self.html))

    def test_get_listing_link(self):
        expected = '/fr/louer/place-parc/neuchatel/st-aubin-sauges/naef-immobilier-neuchatel-115/place-ouverte-380720'
        result = get_listing_link(self.test_listing)
        self.assertEqual(expected, result)

    def test_get_listing_id(self):
        expected = 380720
        result = get_listing_id(self.test_listing)
        self.assertEqual(expected, result)
