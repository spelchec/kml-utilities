import xml.dom.minidom

# Originally from https://developers.google.com/kml/articles/geocodingforkml
# but updated because it is both out of date and much more limited
# (as in, it was only written for a single point).
class KmlBuilder:
    def __init__(self):
        self.kmlDoc = xml.dom.minidom.Document()

    def init(self):
        kmlElement = self.kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
        kmlElement = self.kmlDoc.appendChild(kmlElement)
        kmlElement.setAttributeNS("xmlns", "xmlns", "http://www.opengis.net/kml/2.2")
        # kmlElement.setAttributeNS("xmls", "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        documentElement = self.kmlDoc.createElement('Document')
        self.documentElement = kmlElement.appendChild(documentElement)

    def appendPlacemark(self, placemarkElement):
        self.documentElement.appendChild(placemarkElement)

    def createPlacemarkFromCoordStr(self, coordinates, name, description):
        placemarkElement = self.kmlDoc.createElement("Placemark")
        placemarkElement.appendChild(self.createElementWithText('name', name))
        placemarkElement.appendChild(self.createElementWithText('description', description))
        placemarkElement.appendChild(self.createPointFromCoordStr(coordinates))
        return placemarkElement

    def createPlacemark(self, lat, lon, name, description):
        placemarkElement = self.kmlDoc.createElement("Placemark")
        placemarkElement.appendChild(self.createElementWithText('name', name))
        placemarkElement.appendChild(self.createElementWithText('description', description))
        placemarkElement.appendChild(self.createPoint(lon, lat))
        return placemarkElement

    def createPoint(self, latitude, longitude, altitude = 0):      
        pointElement = self.kmlDoc.createElement("Point")
        coordinatesElement = self.createElementWithText("coordinates", ','.join([str(longitude), str(latitude)]))
        pointElement.appendChild(coordinatesElement)
        return pointElement

    def createPointFromCoordStr(self, coordinates):      
        pointElement = self.kmlDoc.createElement("Point")
        coordinatesElement = self.createElementWithText("coordinates", coordinates)
        pointElement.appendChild(coordinatesElement)
        return pointElement

    def createElementWithText(self, elementName, elementText):
        nameElement = self.kmlDoc.createElement(elementName)
        nameText = self.kmlDoc.createTextNode(elementText)
        nameElement.appendChild(nameText)
        return nameElement

    def build(self, filename):
        # This writes the KML Document to a file.
        kmlFile = open(filename, 'wb')
        kmlFile.write(self.kmlDoc.toprettyxml(' ', ' ', 'UTF-8'))  
        kmlFile.close()
