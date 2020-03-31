import unittest
import yaml
from src.parser.listing import Listing
from src.utilities import response_from_text
from src.config import conf
import os

# This is going to be a base class, and I will subclass
# TestImmobilier etc.  That will let me test things like getText etc.


class TestListing(unittest.TestCase):
    def setUp(self):
        self.parser = Listing(response_from_text('base text'))

    def test_constructor(self):
        print('before', self.parser.response.text)
        new_response = response_from_text('this is some new text')
        self.parser.response = new_response
        print('after', self.parser.response.text)

    def test_AllGetFunctionsOnSnippets(self, v=True):
        def checkGoodInput(test_params):
            input = response_from_text(test_params['input_text'])
            self.parser.setAttributes(input)
            method = test_params['method_to_test']
            result = getattr(self.parser, method)()
            if v:
                print(method, result)
            self.assertEqual(result, test_params['expected'],  test_params['error_message'])

        def checkBadInput(method):
            bad_input = response_from_text('blah')
            self.parser.setAttributes(bad_input)
            result = getattr(self.parser, method)()
            badparser = Listing(bad_input)
            expected = getattr(badparser, method)()
            error_str = '%s did not return correct default + with bad input' % method
            self.assertEqual(result, expected, error_str)

        if self.parser.section == 'DEFAULT':
            return

        test_file = os.path.normpath((conf[self.parser.section]['test_file']))
        print('FILE', test_file)
        with open(test_file, encoding='utf8') as file:

            tests_dict = yaml.load(file, Loader=yaml.FullLoader)

            for k, test_param_dict in tests_dict.items():
                checkGoodInput(test_param_dict)
                checkBadInput(test_param_dict['method_to_test'])
