import requests
import os
import pandas as pd
import sqlalchemy as db
import sys
import datetime
import pytz


API_KEY = os.environ.get('AVIATIONSTACK_API_KEY')

# Authorization Function


def auth_amadeus():
    AUTH_URL = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    auth_response = requests.post(AUTH_URL, {
                                            'grant_type': 'client_credentials',
                                            'client_id':
                                            os.environ.get(
                                                          'AMADEUS_CLIENT_ID'),
                                            'client_secret':
                                            os.environ.get(
                                                 'AMADEUS_CLIENT_SECRET')}
                                  )
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token),
               'X-HTTP-Method-Override': 'GET'}
    return headers

# Function for getting airports


def get_request(headers, city):
    params = {'subType': ['AIRPORT'],
              'keyword': str(city)}
    BASE_URL = 'https://test.api.amadeus.com/v1/reference-data/locations?'\
               'subType=AIRPORT&keyword=' + city + '&view=LIGHT'
    r = requests.get(BASE_URL, headers=headers)
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
        print(str(numbering) + '. ', name, detailed_name, '(' + iataCode + ')')
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
        print(str(numbering) + '. ', name, detailed_name, '(' + iataCode + ')')
        arrive_iata_list.append(iataCode)
        arrive_name_list.append(name)
        numbering += 1


# Validate Date


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD. Please Start Over")
        sys.exit(1)


# POST request for flights FUNCTION


def get_flights_request(headers, departure_airport_iata,
                        arrival_airport_iata, date):
    BASE_URL = 'https://test.api.amadeus.com/v1/shopping/availability/'\
               'flight-availabilities'
    data = {
            "originDestinations": [{"id": "1",
                                    "originLocationCode":
                                    departure_airport_iata,
                                    "destinationLocationCode":
                                    arrival_airport_iata, "departureDateTime":
                                    {"date": date, "time": "21:15:00"}}],
            "travelers": [{"id": "1", "travelerType": "ADULT"}],
            "sources": ["GDS"]}
    auth_response = requests.post(BASE_URL, headers=headers, json=data)
    auth_response_data = auth_response.json()
    return(auth_response_data)

# Function: make list of route iata's for display then prints it for the user


def print_routes(flights_response, flights_list):
    # parse
    try:
        available_routes = flights_response['data']
    except KeyError:
        print("There are no available flights. Please start again.")
        sys.exit()

    # create list of options
    count = 1
    for route in available_routes:
        segments = route['segments']
        flights_list.append({str(count): {}})
        print(str(count) + ". ")
        segment_dict = flights_list[count - 1][str(count)]
        for segment in segments:
            departure_iata = segment['departure']["iataCode"]
            arrival_iata = segment['arrival']["iataCode"]
            segment_name = departure_iata + " -> " + arrival_iata
            segment_dict[segment_name] = [departure_iata,
                                          segment['departure']["at"],
                                          arrival_iata,
                                          segment['arrival']["at"]]
            print(segment_name + "\n\tdepart on: " +
                  flights_list[count - 1][str(count)][segment_name][1][:10] +
                  " Time: " +
                  flights_list[count - 1][str(count)][segment_name][1][11:])
            print("\tarrive on: " + segment['arrival']["at"][:10] +
                  " Time: " + segment['arrival']["at"][11:])
        count += 1


print("Enter departure city: ", end='')
# change this to user input
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

# get the choice
departure_airport_choice = input("Choice: ")
departure_airport_iata = ''
departure_airport_name = ''
try:
    departure_airport_iata = depart_iata_list[
                                             int(departure_airport_choice) - 1]
    departure_airport_name = depart_name_list[
                                             int(departure_airport_choice) - 1]
except IndexError:
    print("Your choice is invalid. Please Start Over.")
    sys.exit()

# now we must get the destination airport
print("Enter a destination city: ", end='')

# change this to user input
arrival_city = input()
head = auth_amadeus()
arrival_airports = get_request(head, arrival_city)

# initialize variables
arrive_iata_list = []
arrive_name_list = []

# display arrival airports
print_arrive_airports(arrive_iata_list, arrive_name_list)

# get the choice
arrival_airport_choice = input("Choice: ")
arrival_airport_iata = ''
arrival_airport_name = ''
try:
    arrival_airport_iata = arrive_iata_list[int(arrival_airport_choice) - 1]
    arrival_airport_name = arrive_name_list[int(arrival_airport_choice) - 1]
except IndexError:
    print("Your choice is invalid. Please Start Over")
    sys.exit()

# get a date from the user
print("Enter your earliest date (yyyy-mm-dd): ", end='')
date = input()
validate(date)

# variables to be used outside of the function
flights_list = []

# call function for POST request to get list of flights
flights_response = get_flights_request(head, departure_airport_iata,
                                       arrival_airport_iata, date)

# display list of available flights
print("Here are flights from " + departure_city + " to " + arrival_city + ": ")
print_routes(flights_response, flights_list)

# Choose a flight
print("Choose a flight (type the number): ", end='')
flight_opt_num = input()

# Overall route
overall_route = departure_airport_iata + " -> " + arrival_airport_iata
# Flight Days vars for weather
try:
    route_list = list(flights_list[int(flight_opt_num) - 1]
                      [flight_opt_num].values())
except IndexError:
    print("Your Selection was invalid. Please Start Over")
    sys.exit()
start_flight_day = route_list[0][1][:10]
end_flight_day = route_list[len(route_list) - 1][1][:10]
# Time of first departure for math
time_of_departure = list(flights_list[int(flight_opt_num) - 1]
                         [flight_opt_num].values())[0][1][11:]
# Timezone handling
zones = pytz.all_timezones
print("Enter the number beside your local time zone:")
num = 1
us_zones = zones[577: 588]
for zone in us_zones:
    print(str(num) + " " + zone)
    num += 1
timezone_num = input("choice: ")
timezone = us_zones[int(timezone_num) - 1]
# name of airports and overall route
print()
print("Your Flight: " + departure_airport_name + " -> " +
      arrival_airport_name + "(" + overall_route + ")")
# departure and arrival city
print("Dearture City:  " + departure_city + "\nArrival City: " + arrival_city)
# day and time for departure
print("Departure Day and Time: " + start_flight_day +
      " at " + time_of_departure)
# connections
print("Flight Connections: ")
for key in flights_list[int(flight_opt_num) - 1][flight_opt_num]:
    print(f'\t{key}')
# get date
local_time = pytz.timezone(timezone)
today = datetime.datetime.now()
fday = datetime.datetime(2022, int(start_flight_day[5:7]),
                         int(start_flight_day[8:]),
                         int(time_of_departure[:2]),
                         int(time_of_departure[3:5]))
time_diff = fday - today
print(f"Your flight is in {time_diff}")

# Weather code


# FUNTION GET_FORECAST, RETURN JSON RESPONSE


def get_forecast(city):
    params = {
        # 'key': os.environ.get('WEATHERAPI_API_KEY'),
        'key': os.environ.get('WEATHERAPI_API_KEY'),
        'q': str(city),
        'days': '1',
        'aqi': "yes",
        'alerts': "yes"}
    BASE_URL = 'https://api.weatherapi.com/v1/forecast.json?'
    r = requests.get(BASE_URL, params)
    return(r.json())


# Collect and display weather info for departure and arrival city
# Variables for departure weather
departure_forecast_data = get_forecast(departure_city)
# holds the weather information in a dictionary in case we want to
# include this information in the database


departure_forecast_dict = {"temp": [],
                           "air_condition": [],
                           "other_conditions": []}
departure_forecast = []
day_forecast_info = departure_forecast_data["forecast"]["forecastday"][0]
count = 0
for key in day_forecast_info['day']:
    val = str(key) + " : " + str(day_forecast_info['day'][key])
    departure_forecast.insert(count, val)
    if key == "condition":
        val = str(key) + " : " + str(day_forecast_info['day']
                                                      ["condition"]
                                                      ["text"])
        departure_forecast.insert(count, val)
    # print(departure_forecast[count])
    count += 1
departure_forecast_dict["temp"] = departure_forecast[0:6]
departure_forecast_dict["air_condition"] = departure_forecast[6:12]
departure_forecast_dict["other_conditions"] = departure_forecast[12:18]

# Variables for arrival weather
arrival_forecast_data = get_forecast(arrival_city)
arrival_forecast_dict = {"temp": [],
                         "air_condition": [],
                         "other_conditions": []}
arrival_forecast = []
day2_forecast_info = departure_forecast_data["forecast"]["forecastday"][0]
count = 0
for key in day2_forecast_info['day']:
    val = str(key) + " : " + str(day2_forecast_info['day'][key])
    arrival_forecast.insert(count, val)
    if key == "condition":
        val = str(key) + " : " + str(day2_forecast_info['day']
                                                       ["condition"]
                                                       ["text"])
        arrival_forecast.insert(count, val)
    # print(departure_forecast[count])
    count += 1
arrival_forecast_dict["temp"] = departure_forecast[0:6]
arrival_forecast_dict["air_condition"] = departure_forecast[6:12]
arrival_forecast_dict["other_conditions"] = departure_forecast[12:18]


def create_database(forecast_info_dict):
    if forecast_info_dict is None:
        return None
    # create dataframe from the extracted records
    forecast_df = pd.DataFrame.from_dict(forecast_info_dict)

    # creating a database from dataframe
    engine = db.create_engine('sqlite:///weather_forcast.db')
    forecast_df.to_sql('forecast_info_dict',
                       con=engine,
                       if_exists='replace',
                       index=False)
    query_result = engine.execute(
                                "SELECT * FROM" +
                                " forecast_info_dict;").fetchall()

    return forecast_df


print("This is the weather for departure city: ", departure_city)
print("date : " + day_forecast_info['date'])
query_result = create_database(departure_forecast_dict)
print((pd.DataFrame(query_result)))

print("This is the weather for arrival city: ", arrival_city)
print("date : " + day2_forecast_info['date'])
query_result2 = create_database(arrival_forecast_dict)
print((pd.DataFrame(query_result2)))
