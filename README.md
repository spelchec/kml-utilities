# kml-utilities

A very simple set of python utilities that I used for some geospacial things.

To run:
```
python geocode_addresses.py
```

### Reading a List of Addresses
Addresses are read from a file looking like this:
```
# list-of-addresses.txt

Empire State Building, New York City, NY.
The White House, Washington DC.
```

This is a very simple application, so a few things to keep in mind:
* It won't be clever with multiple results. You can avoid this by being very explicit with the address.
* It reads a single line as an address. The only exceptions are empty lines, and lines commented up front with `#`.