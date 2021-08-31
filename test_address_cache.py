import address_cache

x = address_cache.AddressCache('mytestcache')

print("Testing AddressCache here")

try:
  addy = x.get_cache('my non-existant location')
  print("There should be nothing here: " + addy)
except TypeError:
  print("this is right!")

CACHED_LOCATION = 'my cached location'
NEVER_CACHED_LOCATION = 'my never cached location'

if not x.is_cached(CACHED_LOCATION):
  print("I should be cached!?")
  addy = x.put_cache(CACHED_LOCATION, 'some text')
else:
  print("I'm caching at " + CACHED_LOCATION)
addy = x.get_cache(CACHED_LOCATION)

TEXT_DONT_CACHE_IT = "I don't know what to write here."
never_cached = x.put_cache(NEVER_CACHED_LOCATION, TEXT_DONT_CACHE_IT)
print("There should be '" + TEXT_DONT_CACHE_IT + "' here: '" + never_cached + "'")

x.show_cache()
