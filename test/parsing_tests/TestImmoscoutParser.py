import unittest
import yaml
from scrapy.selector import Selector
from src.parser.ImmoscoutParser import ImmoscoutParser
from src.utilities import response_from_file, response_from_text
import pandas as pd


class TestImmoscoutParser(unittest.TestCase):
    def setUp(self):
        self.parser = ImmoscoutParser()

    def test_AllGetFunctions(self, v=True):
        test_file_path = 'test\\parsing_tests\\immoscout_gets.yaml'
        with open(test_file_path, encoding='utf8') as file:

            tests_dict = yaml.load(file, Loader=yaml.FullLoader)
            for k in tests_dict.keys():

                test_parameters = tests_dict[k]
                input = response_from_text(test_parameters['input_text'])
                method = test_parameters['method_to_test']
                result = getattr(self.parser, method)(input)
                if v:
                    print(result)
                self.assertEqual(result, test_parameters['expected'], test_parameters['error_message'])
                bad_input = response_from_text('blah')
                method = test_parameters['method_to_test']
                result = getattr(self.parser, method)(bad_input)
                self.assertEqual(result, test_parameters['bad_expected'], 'does not handle bad input')

    def test_getAddress(self):
        test_file = 'test\\parsing_tests\\immoscout_sample_page.html'
        input = response_from_file(test_file)
        result = self.parser.getAddress(input)
        expected = dict(zip(['Street', 'Zip', 'City'], ['Rue du Bugnon 33','1020','Renens']))
        self.assertEqual(expected,result)

    def test_getRooms(self):
        test_file = 'test\\parsing_tests\\immoscout_sample_page.html'
        input = response_from_file(test_file)
        result = self.parser.getRooms(input)
        print(result)
        room_cols = ['chambre', 'séjour', 'cuisine', 'wc', 'hall',
                     'outdoors', 'cave', 'réduit', 'Entrée', 'stores']
        room_counts = [0, 0, 1, 2, 0, 0, 0, 0, 0, 0]
        expected = dict(zip(room_cols, room_counts))
        self.assertEqual(result, expected)
