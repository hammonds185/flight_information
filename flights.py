import requests
import os
API_KEY = os.environ.get('AVIATIONSTACK_API_KEY')

# Authorization Function
def auth_amadeus():
  AUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
  auth_response = requests.post(AUTH_URL, {
  'grant_type': 'client_credentials',
  'client_id': os.environ.get('AMADEUS_CLIENT_ID'),
  'client_secret': os.environ.get('AMADEUS_CLIENT_SECRET')
  })
  auth_response_data = auth_response.json()
  access_token = auth_response_data['access_token']
  headers = {'Authorization': 'Bearer {token}'.format(token=access_token),
  'X-HTTP-Method-Override': 'GET'}
  return headers

#FUNCTION GET_REQUEST, RETURN JSON RESPONSE
def get_request(headers, city):
  params = {'subType': ['AIRPORT'],
    'keyword': str(city)
  }
  BASE_URL = 'https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword=' + city + '&view=LIGHT'
  r = requests.get(BASE_URL, headers = headers)
  return(r.json())

# Print list of airports for user and store info
def print_depart_airports(depart_iata_list, depart_name_list):
  numbering = 1
  name = ''
  detailed_name = ''
  iataCode = ''
  for airport in depart_airports['data']:
    name = airport['name']
    detailed_name = airport['detailedName']
    iataCode = airport['iataCode']
    print(str(numbering) + '. ', name, detailed_name, '('+  iataCode +')')
    depart_iata_list.append(iataCode)
    depart_name_list.append(name)
    numbering += 1

# Print list of airports for user and store info
def print_arrive_airports(arrive_iata_list, arrive_name_list):
  name = ''
  detailed_name = ''
  iataCode = ''
  numbering = 1
  for airport in arrival_airports['data']:
    name = airport['name']
    detailed_name = airport['detailedName']
    iataCode = airport['iataCode']
    print(str(numbering) + '. ', name, detailed_name, '('+  iataCode +')')
    arrive_iata_list.append(iataCode)
    arrive_name_list.append(name)
    numbering += 1

#POST request for flights FUNCTION
def get_flights_request(headers, departure_airport_iata, arrival_airport_iata):
  BASE_URL = 'https://test.api.amadeus.com/v1/shopping/availability/flight-availabilities'
  data = {
    "originDestinations": [
      {
        "id": "1",
        "originLocationCode": "CVG",
        "destinationLocationCode": "LAX",
        "departureDateTime": {
          "date": "2022-07-08",
          "time": "21:15:00"
        }
      }
    ],
    "travelers": [
      {
        "id": "1",
        "travelerType": "ADULT"
      }
    ],
    "sources": [
      "GDS"
    ]
  }
  auth_response = requests.post(BASE_URL, headers=headers, json=data )
  auth_response_data = auth_response.json()
  return(auth_response_data)

# make list of route iata's for display then prints it for the user (FUNCTION)
def print_routes(flights_response, flights_list):
  # parse
  available_routes = flights_response['data']
  #create list of options
  count = 1  
  for route in available_routes:
    segments = route['segments']
    flights_list.append({str(count) : {}})
    print(str(count) + ". ")
    segment_dict = flights_list[count - 1][str(count)]
    for segment in segments:
      departure_iata = segment['departure']["iataCode"]
      arrival_iata = segment['arrival']["iataCode"]
      segment_name = departure_iata + " -> " + arrival_iata
      segment_dict[segment_name] = [departure_iata, segment['departure']["at"], arrival_iata, segment['arrival']["at"]]
      #print(flights_list)
      print(segment_name + "\n depart at: " + flights_list[count - 1][str(count)][segment_name][1] + " -> arrive at: " + segment['arrival']["at"])
    count += 1



print("Enter departure city: ")
#change this to user input
departure_city = input()
head = auth_amadeus()
depart_airports = get_request(head, departure_city)

# have user choose an airport
print("Choose an airport(Type the number beside your choice): ")

# initialize variables
depart_iata_list = []
depart_name_list = []

# call funct to print options
print_depart_airports(depart_iata_list, depart_name_list)

#get the choice
departure_airport_choice = input()
departure_airport_iata = ''
departure_airport_name = ''
try:
  departure_airport_iata = depart_iata_list[int(departure_airport_choice) - 1]
  departure_airport_name = depart_name_list[int(departure_airport_choice) - 1]
except:
  print("Your choice is invalid")

# prints the iata to confirm!!!!!
print(departure_airport_iata)

# now we must get the destination airport
print("Enter a destination city: ")

# change this to user input
arrival_city = input()
head = auth_amadeus()
arrival_airports = get_request(head, arrival_city)

# initialize variables
arrive_iata_list = []
arrive_name_list = []

# display arrival airports
print_arrive_airports(arrive_iata_list, arrive_name_list)

#get the choice
arrival_airport_choice = input()
arrival_airport_iata = ''
arrival_airport_name = ''
try:
  arrival_airport_iata = arrive_iata_list[int(arrival_airport_choice) - 1]
  arrival_airport_name = arrive_name_list[int(arrival_airport_choice) - 1]
except:
  print("Your choice is invalid")

#prints the iata to confirm!!!!!
print(arrival_airport_iata)

# call function for POST request to get list of flights


# variables to be used outside of the function
flights_list = []

# POST request
flights_response = get_flights_request(head, departure_airport_iata, arrival_airport_iata)
#print(flights_response)

# display list of available flights
print("here are flights from " + departure_city + " to " + arrival_city + ": ")
print_routes(flights_response, flights_list)

# Choose a flight
print("Choose a flight: ")
flight_opt_num = input()

# display information
# Name of airports 
  # departure_airport_name
  # arrival_airport_name
# Dearture City
  # departure_city
# Arrival City
  # arrival_city
# Overall route
overall_route = departure_airport_iata + " -> " + arrival_airport_iata
print(overall_route)
# Detailed route
  # the keys in flights_list[int(flight_opt_num) - 1][flight_opt_num]
# Day of First Flight
flight_day = list(flights_list[int(flight_opt_num) - 1][flight_opt_num].values())[0][1][:10]
# Time of first departure 
time_of_departure = list(flights_list[int(flight_opt_num) - 1][flight_opt_num].values())[0][1][11:]
# Time of departures
# Time of arrivals
print(flights_list[int(flight_opt_num) - 1])



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

  