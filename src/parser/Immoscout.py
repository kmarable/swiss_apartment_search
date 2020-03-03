from src.parser import Listing
import re
import html


class ImmoscoutListing(Listing):

    def __init__(self, response):
        self.section = 'IMMOSCOUT'
        self.setAttributes(response)

    def setAttributes(self, response):
        self.response = response
        self.text = self._getText()

    def _getText(self):
        test_text = (self.response.body).decode("utf-8")
        return html.unescape(test_text)

    def getLoyerBrut(self):
        pattern = r'Loyer brut \(mois\)</td><td class=[^>]*>CHF ([^<]+)</td>'
        loyer_line = re.findall(pattern, self.text)
        return self._getFirstInt(loyer_line)

    def getLoyerNet(self):
        pattern = r'Loyer net \(mois\)</td><td class=[^>]*>CHF ([^<]+)</td>'
        loyer_line = re.findall(pattern, self.text)
        return self._getFirstInt(loyer_line)

    def getCharges(self):
        pattern = r'Charges \(mois\)</td><td class=[^>]*>CHF ([^<]+)</td>'
        loyer_line = re.findall(pattern, self.text)
        return self._getFirstInt(loyer_line)

    def getAvailability(self):
        pattern = 'Disponibilit[^<"]*</td><td class=[^>]+>([^<]+)</td>'
        availabilities = re.findall(pattern, self.text)
        return self._getFirstDate(availabilities)

    def getConstructionYear(self):
        c_pattern = 'e de construction</td><td class=[^>]+>([0-9]+)'
        years = re.findall(c_pattern, self.text)
        return self._getSmallestInt(years)

    def getFloor(self):
        pattern = '(Rez-de-chauss[^<]+)</td>'
        floors = re.findall(pattern, self.text)
        if len(floors) > 0:
            return 0
        pattern = 'tage</td><td class=[^>]*>([0-9]+). [^<]+tage</td>'
        floors = re.findall(pattern, self.text)
        return self._getFirstInt(floors)

    def getListingSpace(self):
        pattern = 'Surface habitable</td><td class=[^>]*>([0-9]+) m[^<]+</td>'
        matches = re.findall(pattern, self.text)
        return self._getFirstInt(matches)

    def getAddress(self):
        address_pat = '>Emplacement</h2><p class=[^>]*>([^<]+)<br/>([0-9]{4})<!-- --> <!-- -->([a-zA-Z\s]+)<!-- -->, VD</p>'
        address = re.findall(address_pat, self.text)
        address_dict = {}

        if len(address) == 0:
            return self._getDefaultAddress()
        else:
            new_address = list(address[0])
            new_address[1] = int(new_address[1])  # convert zip to int
            address_dict = dict(zip(['Street', 'Zip', 'City'], new_address))
        return(address_dict)

    def getLatLong(self):
        pattern = '\"latitude\":([0-9.]+),\"longitude\":([0-9.]+)'
        latlong = re.findall(pattern, self.text)
        return self._getFirstLatLong(latlong)

    def getDescription(self):
        #strips html tags and returns the text
        descr = self.response.css('div.sc-7t0e82-0')
        descr_strings = descr.css('p::text').getall()
        return ''.join(descr_strings)

    def getReference(self):
        pattern = 'rence</td><td class=[^>]+>([^<]+)</td>'
        matches = re.findall(pattern, self.text)
        return self._getFirstString(matches).rstrip()

    def getAnnouncer(self):
        pattern = '<td class="sc-1o2xig5-3 bAGQHS"><a href="https?://([^"]+)" target'
        matches = re.findall(pattern, self.text)
        return self._getFirstString(matches)
