import yaml
import os
from scrapy.selector import Selector
from src.utilities import response_from_file, response_from_text

# This takes a parser as a parameter, and calls all the get function cases in the file and checks them against the result provided in the test file.
def helloworld():
    print('hello my friend')

def helloworld2():
    print('hello my friend 2')

def TestAllGetFunctionsOnSnippets(parser, v=True):
    #test_file_path = 'test\\parsing_tests\\immobilier_gets.yaml'
    test_file_path = parser.test_file_path
    with open(test_file_path, encoding='utf8') as file:

        tests_dict = yaml.load(file, Loader=yaml.FullLoader)

        for k in tests_dict.keys():

            test_parameters = tests_dict[k]
            input = response_from_text(test_parameters['input_text'])
            print('the input', input, type(input))
            method = test_parameters['method_to_test']
            result = getattr(parser, method)(input)
            if v:
                print(result)
            assert result == test_parameters['expected'],  test_parameters['error_message']
            bad_input =  response_from_text('blah')
            method = test_parameters['method_to_test']
            result = getattr(parser, method)(bad_input)
            assert result == test_parameters['bad_expected'], 'does not handle bad input'
