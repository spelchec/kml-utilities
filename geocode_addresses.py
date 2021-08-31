import urllib
import urllib.request
import urllib.parse
import json 
import time

import address_loader

from address_cache import AddressCache
from kml_builder import KmlBuilder

# I got some of the initial skeleton from this site:
# https://developers.google.com/kml/articles/geocodingforkml
# but it is unfortunately very out of date at this point.
# Therefore I'm posting my own implementation to ensure that if
# someone (like myself) needs this functionality, they can look
# at something slightly less out of date.

# This is a cache to prevent repetitive requests to Google's APIs,
# and avoid unnecessary charges.
cache = AddressCache("google_geocoding")

# Convenience class around an XML builder.
kmlBuilder = KmlBuilder()

# Reads addresses from a file using the AddressLoader class.
def read_addresses_from_file():
  x = address_loader.AddressLoader('list-of-addresses.txt')
  print("Testing AddressLoader here")
  addresses = []
  while True:
    address = x.get_address()
    if address == "":
      break
    print("Adding address: '" + address + "'")
    addresses += [address]
  return addresses

# Dummy method for testing, if you want it.
def geocode_dummy(address, sensor=False):
  file = open("response-sample.json","r") 
  jsonOutput = str(file.read())
  jsonOutput=jsonOutput.replace ("\\n", "")
  result = json.loads(jsonOutput) # converts jsonOutput into a dictionary 
  if result['status'] != "OK": 
    return ""
  coordinates=result['results'][0]['geometry']['location'] # extract the geometry 
  return ",".join([str(coordinates['lng']), str(coordinates['lat'])])

# This function queries the Google Maps API geocoder with an
# address. It gets back a json response, which it caches for the future.
def get_api_data(address, sensor=False):
  if cache.is_cached(address):
    return cache.get_cache(address,'r')

  # To use the Geocode API you have to set up an account: https://code.google.com/apis/console/
  mapsKey = ''
  mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='

  url = ''.join([mapsUrl,urllib.parse.quote(address),'&sensor=',str(sensor).lower(), '&key=',mapsKey])
  jsonOutput = str(urllib.request.urlopen(url).read(), 'utf-8')
  jsonOutput=jsonOutput.replace("\\n", "")
  jsonOutput = cache.put_cache(address, jsonOutput)

  # Add a small delay to avoid potentially getting throttled.
  time.sleep(2)

  return jsonOutput

# Given an address get the coordinates.
def geocode(address, sensor=False):

  # Get the JSON Output, either from Google or cached.
  jsonOutput = get_api_data(address)
  print("> working with " + jsonOutput)
  result = json.loads(jsonOutput) # converts jsonOutput into a dictionary 
  # check status is ok i.e. we have results (don't want to get exceptions)
  if result['status'] != "OK": 
    return ""
  coordinates=result['results'][0]['geometry']['location'] # extract the geometry 
  return ','.join([str(coordinates['lng']), str(coordinates['lat'])])

def createPlacemarkElement(address):
  coordinates = geocode(address) # geocode_dummy for testing
  placemarkElement = kmlBuilder.createPlacemarkFromCoordStr(coordinates, address, address)
  return placemarkElement

# This builds a KML Document and adds a set of Points based on geographic addresses.
def createKML(addresses, fileName):
  kmlBuilder.init()
  for address in addresses:
    kmlBuilder.appendPlacemark(createPlacemarkElement(address))

  kmlBuilder.build(fileName)

if __name__ == '__main__':
  addresses = read_addresses_from_file()
  print("> Addresses we're going through! " + ';'.join(map(str, addresses)))
  createKML(addresses, 'google.kml')

