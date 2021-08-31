import time

# pulls addresses from a file. Assumes one address per line,
# and ignores empty lines or lines starting with a '#'.
class AddressLoader:
  def __init__(self, location):
    self.file = open(location, "r")
    self.last = None

  def is_address(self, line):
    opline = self.__clean(line)
    is_empty = (opline == "")
    is_comment = opline.startswith("#")
    # print(": {} {}", is_empty, is_comment, "'" + line + "'")
    return not is_empty and not is_comment

  def __clean(self, input):
    return input.strip().replace('\n', '').replace('\r', '')

  def get_address(self):
    # time.sleep(2)
    while True:
      line = self.file.readline()
      if self.is_address(line):
        self.last = line
        return self.__clean(line)
      if line == self.last:
        return self.__clean(line)
      if line == "":
        return line
