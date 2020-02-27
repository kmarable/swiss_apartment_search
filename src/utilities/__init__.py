from scrapy.http import TextResponse, Request
from googlemaps.geocoding import geocode
import pandas as pd
import yaml
import re


def extract_french_number(num_string_list):
    if len(num_string_list) == 0:
        return -1
    defrenched = ''.join([p.replace('\'', '') for p in num_string_list[0]])
    price = re.findall('[0-9]+', defrenched)[0]
    return int(price)


def load_raw_data(arg):
    with open('config.yaml', encoding='utf8') as file:
        params = yaml.load(file, Loader=yaml.FullLoader)
        return(params)

    raw_file = params[0]


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
            final_expression = final_expression + '[-\s]'
        else:
            final_expression = final_expression+j
    return final_expression
