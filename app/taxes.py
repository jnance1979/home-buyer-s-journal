import requests
import os
from requests.exceptions import ConnectionError


def property_characteristics(user_address):

    API_KEY = os.getenv('API_KEY')              # API call to google for geocoding data 

    params = {
        'key': API_KEY,
        'address': user_address
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    response = requests.get(base_url, params=params)
    data = response.json()
    condo = False
    
    if data['status'] == 'OK':
        if data['results'][0]['address_components'][0]['types'] == ['subpremise']:      # reformat data for condos (depending on subpremise) 
            condo = True
            num = data['results'][0]['address_components'][1]['short_name']
            street = (data['results'][0]['address_components'][2]['short_name']).upper()
            start_unit = data['results'][0]['address_components'][0]['short_name']
            split_unit = start_unit.split(' ')
            unit = (split_unit[-1]).upper()
        else:
            num = data['results'][0]['address_components'][0]['short_name']                 # reformat data for houses
            street = (data['results'][0]['address_components'][1]['short_name']).upper()

    else:
        return False
    
    APP_TOKEN = os.getenv('APP_TOKEN')
    def get_pin():
        if condo:
            base_url = f"https://datacatalog.cookcountyil.gov/resource/c49d-89sn.json?$$app_token={APP_TOKEN}&property_address={num} {street}&property_apt_no={unit}"
        else:
            base_url = f"https://datacatalog.cookcountyil.gov/resource/c49d-89sn.json?$$app_token={APP_TOKEN}&property_address={num} {street}"
        try:
            response = requests.get(base_url, None)
            prop = response.json()                      # retrieve property pin and convert to dashed format
            if prop:
                pin = prop[0]['pin']
                d_pin='-'.join([pin[:2], pin[2:4], pin[4:7], pin[7:10], pin[10:]])
                both = [pin, d_pin]
                
            else:                                       # else no information returned from county database
                pin = 'not available'
                d_pin = 'not available'
                both = [pin, d_pin]                
            return both
        except:                                         # in the event of error from county database
            pin = 'not available'
            d_pin = 'not available'
            both = [pin, d_pin]
            return both
    both_pins = get_pin()

    def get_taxes(d_pin):
        # test_pin = '17-08-124-035-1011'
        base_url = f'https://datacatalog.cookcountyil.gov/resource/tnes-dgyi.json?$$app_token={APP_TOKEN}&pin={d_pin}&year=2019'
        try:
            response = requests.get(base_url, None)     # retrieve property assessment amount based on 2019 data (pre-covid discounts)
            assmnts = response.json()
            # print (assmnts)
            prop_value = int(assmnts[0]['bor_result'])
            taxes = round(((prop_value)*3.2234*.06911), 2)      # multiply assessment amount by 2021 IL state equalization factor 
            return taxes                                           # and by 2020 average property tax rate for Chicago  
        except:
            taxes = 0.00
            return taxes
    est_taxes = get_taxes(both_pins[1])
    tax_dict = {
        'pin': both_pins[0],
        'dashed_pin': both_pins[1],
        'taxes': est_taxes
    }

    return tax_dict