# reference
# https://github.com/Yelp/yelp-fusion/tree/master/fusion/python

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import secrets

API_KEY = secrets.API_KEY
exchange_rate_api = secrets.exchange_rate_api
# city_list = ['Detroit, MI', 'Lansing, MI']
city_list = ['Detroit, MI', 'Lansing, MI', 'Ann Arbor, MI', 'Dearborn, MI', 'Flint, MI', 'Warren, MI',
    'Muskegon, MI', 'Kentwood, MI', 'Kalamazoo, MI', 'Grand Rapids, MI']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


SEARCH_LIMIT = 10    # 50


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')
    # print(businesses)
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    json_str = "\"" + location + "\": ["
    for i in range(len(businesses)):
        business_id = businesses[i]['id']
        response = get_business(API_KEY, business_id)
        temp_str = json.dumps(response)
        json_str += temp_str
        if i != len(businesses)-1:
            json_str += ", "
    json_str += "]"
    # print(json_str)
    text_file = open("data.json", "a")
    text_file.write(json_str)
    text_file.close()


def main():
    DEFAULT_TERM = 'chinese'
    text_file = open("data.json", "w")
    json_str = "{\"yelp\": {"
    text_file.write(json_str)
    text_file.close()



    for i in city_list:
        if i != city_list[0]:
            text_file = open("data.json", "a")
            text_file.write(', ')
            text_file.close()
        DEFAULT_LOCATION = i
        parser = argparse.ArgumentParser()

        parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')

        input_values = parser.parse_args()

        try:
            query_api(input_values.term, input_values.location)
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )
    text_file = open("data.json", "a")
    json_str = "}}"
    text_file.write(json_str)
    text_file.close()


if __name__ == '__main__':
    main()