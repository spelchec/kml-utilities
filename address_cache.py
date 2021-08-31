import os
import urllib

from os import path
from urllib.parse import quote

# A simple cache for address information. This is because Google's Geocode APIs
# are expensive, so this will encourage fewer unnecessary requests (because it
# will pull from the cache instead).
class AddressCache:

  def __init__(self, location = "cache"):
    self.debug = False
    self.location = location
    if not path.exists(location):
      os.mkdir(location)

  def __get_cache_name(self, name):
    location = quote(self.location + '/' + urllib.parse.quote(name))
    if self.debug:
      print("> cache " + location)
    return location

  def __has_cache(self, name):
    return path.exists(self.__get_cache_name(name))

  def is_cached(self, name):
    if self.__has_cache(name):
      return True
    return False

  def put_cache(self, name, input, mode = 'w'):
    filename = self.__get_cache_name(name)
    file = open(filename, mode)
    file.write(input)
    file.close()
    return input

  def get_cache(self, name, mode = 'r'):
    filename =self.__get_cache_name(name)
    if self.is_cached(name):
      file = open(filename, mode)
      data = file.read()
      file.close()
      return data

  def invalidate_cache(self, name):
    filename = self.__get_cache_name(name)
    os.remove(filename)

  def show_cache(self):
    print("This is the cache " + self.location + ":")
    print(os.listdir(self.location))
