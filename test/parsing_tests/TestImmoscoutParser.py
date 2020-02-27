import sys

sys.path.append('C:\\Users\\Kathryn\\Documents\\2github\\swiss_apartment_search')
print(sys.path)

from src.parser.ImmoscoutParser import ImmoscoutParser
from src.utilities import response_from_file

testparser = ImmoscoutParser()

test_response = response_from_file('immoscout_sample_page.html')
prix = testparser.getLoyerBrut(test_response)

print('Brut', prix)

prix = testparser.getLoyerNet(test_response)
print('Net', prix)


prix = testparser.getCharges(test_response)

print('Charges', prix)

date = testparser.getAvailability(test_response)

print('DATE', date)

floor = testparser.getFloor(test_response)
print('floor', floor)

space = testparser.getListingSpace(test_response)
print('space', space)

addy = testparser.getAddress(test_response)
print('address', addy)

latlong = testparser.getLatLong(test_response)
print('latlong', latlong)

descr = testparser.getDescription(test_response)
print('descr', descr)

rooms = testparser.getRooms(test_response)
print('rooms', rooms)
