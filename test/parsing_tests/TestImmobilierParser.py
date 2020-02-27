import unittest
import yaml
from scrapy.selector import Selector
from src.parser.ImmobilierParser import ImmobilierParser
import pandas as pd


class TestImmobilierParser(unittest.TestCase):
    def setUp(self):
        self.parser = ImmobilierParser()

    def testNoAssets(self):
        result = self.parser.getListingAssets(Selector(text='lol'))
        self.assertEqual(result, '')

    def test_AllGetFunctions(self, v=True):
        test_file_path = 'test\\parsing_tests\\immobilier_gets.yaml'
        with open(test_file_path, encoding='utf8') as file:

            tests_dict = yaml.load(file, Loader=yaml.FullLoader)
            for k in tests_dict.keys():

                test_parameters = tests_dict[k]
                input = Selector(text=test_parameters['input_text'])
                method = test_parameters['method_to_test']
                result = getattr(self.parser, method)(input)
                if v:
                    print(result)
                self.assertEqual(result, test_parameters['expected'], test_parameters['error_message'])
                bad_input = Selector(text='blah')
                method = test_parameters['method_to_test']
                result = getattr(self.parser, method)(bad_input)
                self.assertEqual(result, test_parameters['bad_expected'], 'does not handle bad input')

    def test_getAddress(self):
        test_file = 'test\\parsing_tests\\address_test.html'
        with open(test_file, encoding='utf8') as file:
            input_text = file.read()
        file.close()
        input = Selector(text=input_text)
        result = self.parser.getAddress(input)
        expected = dict(zip(['Street', 'Zip', 'City'], ['Chemin de Rionza 17', '1020', 'Renens']))
        self.assertEqual(expected,result)

    def test_getRooms(self):
        input_text = "<div class='im__postContent__body'><p>" \
                      "Joli appartement de 3.5 pièces au 2ème étage" \
                      "d'une surface totale de 72m2 comprenant :" \
                      "<BR><BR>- deux chambres à coucher<BR>- un" \
                      "salon <BR>- une cuisine semi-agencée (frigo)"\
                      "<BR>- une salle de bain<BR>- un WC séparé<BR>"\
                      "- 3 balcons<BR> - stores  -un spacieux  " \
                      "r&#233;duit  <BR><BR></p></div>"
        input = Selector(text=input_text)
        result = self.parser.getRooms(input)
        room_cols = ['chambre', 'séjour', 'cuisine', 'wc', 'hall',
                     'outdoors', 'cave', 'réduit', 'Entrée', 'stores']
        room_counts = [[2], [0], [1], [1], [0], [3], [0], [1], [0], [1]]
        expected = pd.DataFrame(dict(zip(room_cols, room_counts)))
        pd.testing.assert_frame_equal(result, expected)
