import yaml
from src.utilities import response_from_text

# This takes a listing class as a parameter
# It looks up the test case file for that class
# Each test case in the file provides sample input and the function to call
# the result is then checked against the result provided in the test file.


def TestAllGetFunctionsOnSnippets(parser, v=True):
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
            bad_input = response_from_text('blah')
            method = test_parameters['method_to_test']
            result = getattr(parser, method)(bad_input)
            assert result == test_parameters['bad_expected'], 'does not handle bad input'
