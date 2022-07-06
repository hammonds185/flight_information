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
    'keyword': str(city)
  }
  BASE_URL = 'https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword=' + city + '&view=LIGHT'
  r = requests.get(BASE_URL, headers = headers)
  return(r.json())
  
#print(get_request(auth_amadeus()))





# def get_city_iata(API_KEY):
#   #dep_iata, arr_iata
#   params = {'access_key': API_KEY,
#   'limit': '1',
#   }
#   CITY_URL = 'http://api.aviationstack.com/v1/cities'
#   r = requests.get(CITY_URL, params)
#   return(r.json())
# def get_flight_info(API_KEY):
#   FLIGHT_URL= 'http://api.aviationstack.com/v1/flights/'
#   params = {'access_key': API_KEY,
#   'flight_date': '2022-07-3',
#   }
#   r = requests.get(FLIGHT_URL, params)
#   return(r.json())

#FUNCTION GET_REQUEST, RETURN JSON RESPONSE
def get_flights_request(API_KEY, dep_iata, arr_iata):
  params = {'access_key': API_KEY,
    'limit': '10',
    'flight_status': 'scheduled',
    'dep_iata': str(dep_iata),
    'arr_iata': str(arr_iata)
  }
  BASE_URL = 'http://api.aviationstack.com/v1/flights'
  r = requests.get(BASE_URL, params)
  return(r.json())

#FUNTION GET_FORECAST, RETURN JSON RESPONSE
def get_forecast(city):
  params = {
    'key': os.environ.get('WEATHERAPI_API_KEY'),
    'q': str(city),
    'days': '1',
    'aqi': "yes",
    'alerts': "yes"
  }
  BASE_URL = 'https://api.weatherapi.com/v1/forecast.json?'
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

#prints the iata to confirm!!!!!
print(departure_airport_iata)

# now we must get the destination airport
print("Enter a destination city: ")
#change this to user input
arrival_city = input()
head = auth_amadeus()
arrival_airports = get_request(head, arrival_city)

print("here are flights from " + departure_city + " to " + arrival_city + ": ")

# initialize variables
name = ''
detailed_name = ''
iataCode = ''
iata_list = []
#numbering = 1

#Print list of airports for user and store info
#start here
for airport in arrival_airports['data']:
  name = airport['name']
  detailed_name = airport['detailedName']
  iataCode = airport['iataCode']
  #instead of printing the info we must use the iatas as parameters for aviationstack
  # I printed name to see what airport is going into the aviationstack request
  print(name)
  # the request
  available_flights = get_flights_request(API_KEY, departure_airport_iata, iataCode)
  # parsing data to get each fight date, departure place, and arrival place
  data = available_flights['data']
  for flight in data:
    print(flight['flight_date'])
    print(flight['departure']['airport'])
    print(flight['arrival']['airport'])
    print("\n")


# Collect and display weather info for departure and arrival city 
# Variables for departure weather 
departure_forecast_data = get_forecast(departure_city)
#holds the weather information in a dictionary in case we want to 
#include this information in the database 
departure_forecast = {}
day_forecast_info = departure_forecast_data["forecast"]["forecastday"][0]

print("This is the weather for departure city: " , departure_city)
print("date : " + day_forecast_info['date'])
for key in day_forecast_info['day']:
  if key == "condition":
    departure_forecast[key] = day_forecast_info['day']["condition"]["text"]
  departure_forecast[key] = day_forecast_info['day'][key]
  print(key, ":", departure_forecast[key])

# Variables for arrival weather 
arrival_forecast_data = get_forecast(arrival_city)
arrival_forecast = {}
day2_forecast_info = arrival_forecast_data["forecast"]["forecastday"][0]

print("This is the weather for arrival city: " , arrival_city)
print("date : " + day2_forecast_info['date'])
for key in day2_forecast_info['day']:
  if key == "condition":
    arrival_forecast[key] = day2_forecast_info['day']["condition"]["text"]
  arrival_forecast[key] = day2_forecast_info['day'][key]
  print(key, ":", arrival_forecast[key])

  