"""
generate_sample_data generates sample data based on real FX rate and
save into sample_data.json
"""
import http.client
import json
import random
from datetime import datetime, date, timedelta

def generate_sample_data(sample_count):
    """
        grab the currency data from the web api and save into sample_data.json
        Args:
            sample_count:
                how many items in the sample_data.json
        Returns:
            the sample_data in memory
    """

    currency_data = grab_currency_data_from_internet()
    currency_data = convert_currency_format(currency_data)
    result = []
    currency_list = list(currency_data.keys())
    start_date = date.today().replace(day=1, month=1).toordinal()
    end_date = date.today().toordinal()
    for i in range(sample_count):
        currency_type = random.choice(currency_list)
        random_day = date.fromordinal(random.randint(start_date, end_date))
        result.append({
            'entity': 'foo{}'.format(i),
            'buy_sell': random.choice(['B', 'S']),
            'fx': currency_data[currency_type],
            'currency': currency_type,
            'ins_date': random_day,
            'set_date': settlement_date(currency_type, random_day),
            'units': random.randrange(100, 1000),
            'unit_price': random.randrange(100, 50000) / 100,
            })

    return result

def grab_currency_data_from_internet():
    """
    grab the currency data from the web api

    Returns:
        raw currency data
    """
    try:
        import secret
    except ImportError:
        print('Missing config.py, if you just cloned this repo, please rename\
            the config.example.py to config.py and set access_key. To get the\
            key, please go to https://currencylayer.com/')
        raise

    http_connection = http.client.HTTPConnection('www.apilayer.net')
    http_connection.request(
        'GET', '/api/live?access_key={}'.format(secret.access_key))
    response = http_connection.getresponse()
    if response.status != 200:
        raise RuntimeError('internet issue')

    return json.loads(response.read().decode('utf-8'))['quotes']
    
def convert_currency_format(currency_data):
    """
    convert currency data from web raw format to local format
    Args:
        currency_data: dict from www.apilayer.net
    Returns:
        local format dict of FX
    """
    result = {}
    for key in currency_data:
        new_key = key[3:]
        new_val = 1/currency_data[key]
        result[new_key] = new_val
    return result

def settlement_date(currency, instruction_date):
    """
    calculate the first available date for settlement
    """
    if currency in ['AED', 'SAR']:
        invalid_day = [4,5]
    else:
        invalid_day = [5,6]
    weekday = instruction_date.weekday()
    if weekday == invalid_day[0]:
        return instruction_date + timedelta(days=2)
    elif weekday == invalid_day[1]:
        return instruction_date + timedelta(days=1)
    else:
        return instruction_date


