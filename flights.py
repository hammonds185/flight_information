import requests
import os

API_KEY = os.environ.get('AVIATIONSTACK_API_KEY')

def auth_amadeus():
  AUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
  auth_response = requests.post(AUTH_URL, {
  'grant_type': 'client_credentials',
  'client_id': os.environ.get('AMADEUS_CLIENT_ID'),
  'client_secret': os.environ.get('AMADEUS_CLIENT_SECRET')
  })
  auth_response_data = auth_response.json()
  access_token = auth_response_data['access_token']
  headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
  return headers


#FUNCTION GET_REQUEST, RETURN JSON RESPONSE
def get_request(headers, city):
  params = {'subType': ['AIRPORT'],
    'keyword': 'Cincinnati'
  }
  BASE_URL = 'https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword=' + city + '&view=LIGHT'
  r = requests.get(BASE_URL, headers = headers)
  return(r.json())
  
#print(get_request(auth_amadeus()))





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


# result = get_flights_request(API_KEY)
# data = result['data']
# for flight in data:
#   print(flight)
#   print("\n")

#This is where calls start
print("Enter departure city: ")
#change this to user input
departure_city = input()
head = auth_amadeus()
depart_airports = get_request(head, departure_city)

# have user choose an airport
print("Choose an airport(Type the number beside your choice): ")

# initialize variables
name = ''
detailed_name = ''
iataCode = ''
iata_list = []
numbering = 1

# Print list of airports for user and store info
for airport in depart_airports['data']:
  name = airport['name']
  detailed_name = airport['detailedName']
  iataCode = airport['iataCode']
  print(str(numbering) + '. ', name, detailed_name, '('+  iataCode +')')
  iata_list.append(iataCode)
  numbering += 1

#get the choice
departure_airport_choice = input()
departure_airport_iata = ''
try:
  departure_airport_iata = iata_list[int(departure_airport_choice) - 1]
except:
  print("Your choice is invalid")

#prints the iata to confirm
print(departure_airport_iata)



