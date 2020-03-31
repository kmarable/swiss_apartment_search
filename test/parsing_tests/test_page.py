import unittest
import datetime
import re
from src.utilities.htmlFile import htmlFile
from src.utilities import response_from_text
from src.parser.Immobilier import ImmobilierListing


class TestImmobilierOnPage(unittest.TestCase):

    def setUp(self, filename=''):
        file_name = 'test\\parsing_tests\\immobilier_sample_page.html'
        #file_name = 'data\\saved_pages\\2020-03-04_385220.html'
        self.file = htmlFile(file_name)
        self.response = response_from_text(self.file.read()['BODY'])
        self.listing = ImmobilierListing(self.response)

    def test_header(self):
        headerData = self.file.read()['HEADER'].__dict__
        expected = {'link': 'https://www.immobilier.ch/fr/louer/appartement/vaud/lausanne/livit-ag-real-estate-management-675/lumineux-logement-381825', 'id': 381825, 'host': 'Immobilier', 'date': '2020-02-26'} # noqa
        self.assertEqual(headerData, expected, 'did not read header')

    def test_getAvailability(self):
        expected = datetime.datetime(2020, 3, 1)
        error = 'did not get availabiltiy'
        result = self.listing.getAvailability(v=True)
        print(result)
        self.assertEqual(result, expected, error)

    def test_characters(self):
        res = re.findall('Disponible d[^<]+<', self.response.text)
        print( 'res', res)
