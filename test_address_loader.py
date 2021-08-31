import address_loader

x = address_loader.AddressLoader('list-of-addresses.txt')

print("Testing AddressLoader here")

while True:
  addy = x.get_address()
  print("line --- '" + addy + "'")
  if addy == "":
    break