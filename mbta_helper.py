import urllib.request
import json
from pprint import pprint
import ssl
"""Ensures secure communication"""
ssl._create_default_https_context = ssl._create_unverified_context

"""URLS for requests"""
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

"""API KEYS we retrieved from respective websites"""
MAPQUEST_API_KEY = "OyNGQIQaGmnhZ7MONyGqtgwArSMe6QA8"
MBTA_API_KEY = "68b2a7ae63184c6c930c23dd6940c075"

def get_json(url):
    """
    This function returns Python JSON object containing the response to that request for the purpose of either MBTA or Mapquest
    """
    f = urllib.request.urlopen(url)
    text_response = f.read().decode('utf-8')
    response_data = json.loads(text_response)
    return response_data


def get_lat_long(place_name):
    """
    This function returns latitude and longitude after inputting place in Boston
    """
    place_name = str(place_name)
    place_name = place_name.replace(" ", "%20")
    place_name = f"{place_name},MA"
    """Ensure place is in Mass"""
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}'
    json_text = get_json(url)
    coordinates_lat_long = json_text["results"][0]["locations"][0]["latLng"]
    latitude = coordinates_lat_long["lat"]
    longitude = coordinates_lat_long["lng"]
    return latitude, longitude


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude, utilizes MBTA API in order to return nearest MBTA station name and wheelchair accessibility of the station
    """
    url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    data = get_json(url)
    try:
        place = data["data"][0]["attributes"]["name"]
        wheelchair_accessibility = data["data"][0]["attributes"]["wheelchair_boarding"]
    except:
        return "MBTA Not Available"
    if wheelchair_accessibility == 0:
        wheelchair_accessibility = "No Information"
    elif wheelchair_accessibility == 1:
        wheelchair_accessibility = "Accessible"
    else:
        wheelchair_accessibility = "Inaccessible"
    return f"Station: {place}, Wheelchair Accessibility: {wheelchair_accessibility}"


def find_stop_near(place_name):
    """
    Final function, where according to latitude and longitude of place name, nearest station and wheelchair accessibility of the station is outputted
    """
    location_data = get_lat_long(place_name)
    latitude = location_data[0]
    longitude = location_data[1]
    return get_nearest_station(latitude, longitude)


def main():
    """
    Test code - where place name is user input and final function is used to output nearest station and wheelchair accessibility of the station
    """
    place = str(input("Please enter your location: "))
    print(find_stop_near(place))


if __name__ == '__main__':
    main()