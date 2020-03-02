import unittest
import yaml
from scrapy.selector import Selector
from src.parser.ImmobilierParser import ImmobilierParser
import pandas as pd
import sys
import test.parsing_tests.test_utilities as utils



class TestImmobilierParser(unittest.TestCase):
    def setUp(self):
        self.parser = ImmobilierParser()

    def testNoAssets(self):
        result = self.parser.getListingAssets(Selector(text='lol'))
        self.assertEqual(result, '')

    def test_AllGetFunctions(self, v=True):
        utils.TestAllGetFunctionsOnSnippets(self.parser)


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
        room_counts = [2, 0, 1, 1, 0, 3, 0, 1, 0, 1]
        print(room_counts)
        expected = dict(zip(room_cols, room_counts))
        self.assertEqual(result, expected)
