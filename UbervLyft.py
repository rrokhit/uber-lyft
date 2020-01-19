import requests
from geopy.geocoders import Nominatim
import pdb
from pprint import pprint

locator = Nominatim(user_agent='myGeocoder')

#turns address into a tuple, of form,: latitude, longitude
def get_coordinates(address):
    location = locator.geocode(address)
    return location.latitude,location.longitude

#Enter addresses in the following format: '123 Some Street, City, Country'
def get_lyft_fare(source_address,destination_address):
    source_latitude, source_longitude = get_coordinates(source_address)
    destination_latitude, destination_longitude = get_coordinates(destination_address)
    parameters = {
        'start_lat': source_latitude,
        'start_lng': source_longitude,
        'end_lat': destination_latitude,
        'end_lng': destination_longitude
        }
    r = requests.get(url = 'https://www.lyft.com/api/costs', params = parameters)
    pprint (r.json())


def get_uber_address_ids(session, address):
    headers = {
        'content-type':'application/json',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-csrf-token':'x'
        }
    #params
    body = {
            "type":"pickup",
            "q":address,
            "locale":"en"
            }
    response= session.post(url = 'https://www.uber.com/api/loadFESuggestions', headers = headers , json = body)
    r_dict = response.json()
    id_list = [suggestion['id'] for suggestion in r_dict['data']['candidates']]
    return id_list
        
    
    


def get_uber(source_address,destination_address):

    source_latitude, source_longitude = get_coordinates(source_address)
    destination_latitude, destination_longitude = get_coordinates(destination_address)
    headers={"Accept":"text/html"}
    session = requests.Session()
    session.get('https://www.uber.com/ca/en/price-estimate/', headers= headers)
    #for the cookies
    #session has the cookie for that site

    origin_id= get_uber_address_ids(session, source_address)[0]
    destination_id= get_uber_address_ids(session, destination_address)[0]

    headers = {
                'x-csrf-token':'x',
                'origin':'https://www.uber.com',
                'referer':'https://www.uber.com/ca/en/price-estimate/',
                'sec-fetch-mode':'cors', 'sec-fetch-site':'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                'content-type': 'application/json'
                }
    #params
    body ={
        'destination': {
                 'id': destination_id,
                 'latitude':  destination_latitude,
                 'locale': 'en',
                 'longitude':destination_longitude,
                 'provider': 'google_places'
                 },
         'locale': 'en',
         'origin': {
                    'id': origin_id,
                    'latitude': source_latitude,
                    'locale': 'en',
                    'longitude': source_longitude,
                    'provider': 'google_places'
                    }
        }
    r = session.post(url = 'https://www.uber.com/api/loadFEEstimates', headers = headers ,  json=body)
    pprint(r.json())
