import requests
import os
API_KEY = '83b7473de92bc4b9cc05065ed7daf92d'
def get_city_iata(API_KEY):
  #dep_iata, arr_iata
  params = {'access_key': API_KEY,
  'limit': '1',
  }
  CITY_URL = 'http://api.aviationstack.com/v1/cities'
  r = requests.get(CITY_URL, params)
  return(r.json())
def get_flight_info(API_KEY):
  FLIGHT_URL= 'http://api.aviationstack.com/v1/flights/'
  params = {'access_key': API_KEY,
  'flight_date': '2022-07-3',
  }
  r = requests.get(FLIGHT_URL, params)
  return(r.json())

#FUNCTION GET_REQUEST, RETURN JSON RESPONSE
def get_flights_request(API_KEY):
  #API_KEY = '83b7473de92bc4b9cc05065ed7daf92d'
  params = {'access_key': API_KEY,
    'limit': '10',
    'flight_status': 'scheduled',
    'dep_iata': 'CVG',
    'arr_iata': 'MIA'
  }
  BASE_URL = 'http://api.aviationstack.com/v1/flights'
  r = requests.get(BASE_URL, params)
  return(r.json())


result = get_flights_request(API_KEY)
data = result['data']
for flight in data:
  print(flight)
  print("\n")



