from scrapy.http import TextResponse, Request
import pandas as pd
import re
import os
import inspect


def get_absolute_path(file_name):
    folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    print(folder)
    return(os.path.join(folder, os.path.normpath(file_name)))


def get_get_functions(class_):
    def isPublic(name):
        return name[0] != '_'

    def isGet(name):
        return 'get' in name
    methods = inspect.getmembers(class_)
    method_names = [m[0] for m in methods if isGet(m[0]) and isPublic(m[0])]
    return method_names


def extract_french_number(num_string):
    if len(num_string) == 0:
        return -1
    defrenched = ''.join([p.replace('\'', '') for p in num_string])
    price = re.findall('[0-9]+', defrenched)[0]
    return int(price)


def response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """

    file = open(file_name, 'r', encoding='utf-8')
    file_content = file.read()
    file.close()

    response = response_from_text(file_content)
    return response


def response_from_text(text, url=None):
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)

    response = TextResponse(url=url, request=request,
                            body=text, encoding='utf-8')

    return response


def dictListToDataFrame(listOfDicts):
    df = pd.DataFrame()
    key_list = listOfDicts[0].keys()
    for k in key_list:
        df[k] = [l[k] for l in listOfDicts]
    return df


def make_case_insensitive(pattern):

    opp_letters = [p.upper() for p in pattern]
    final_expression = ''
    for i, j in zip(opp_letters, pattern):
        if i.isalpha():
            final_expression = final_expression + '[' + i + j + ']'
        elif i == '-':
            final_expression = final_expression + r'[-\s]'
        else:
            final_expression = final_expression+j
    return final_expression
