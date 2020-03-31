from src.parser.listing import Listing
import re


class ImmobilierListing(Listing):

    def __init__(self, response, v=False):
        self.section = 'IMMOBILIER'
        self.setAttributes(response)
        self.v = v

    def setAttributes(self, response):
        self.response = response
        self.assets = self._getListingAssets()

    def _getListingAssets(self):
        assets = self.response.css('div.im__assets__table').get()
        if assets is None:
            return ''
        else:
            return assets

    def getAvailability(self):
        # returns 1970 if not found
        # will convert to download date in post-processing
        pattern = r'Disponible d.s\s*(.*\s*[0-9]+)\s*<'
        availabilities = re.findall(pattern, self.assets)
        if self.v:
            print(availabilities)
        return self._getFirstDate(availabilities)

    def getConstructionYear(self):
        c_pattern = r'onstruit en\s*([0-9]*)[\s\t]*'
        years = re.findall(c_pattern, self.assets)
        return self._getFirstInt(years)

    def getFloor(self):
        if re.search(r'Rez-de-chaussée', self.assets):
            return 0
        floors = re.findall(r'([2-9])ème étage', self.assets)
        floors.extend(re.findall(r'(1)er étage', self.assets))
        return self._getFirstInt(floors)

    def getLoyerNet(self):
        loyer_line = re.findall('Loyer : CHF [0-9\']*.-/mois', self.assets)
        return self._getFirstInt(loyer_line)

    def getCharges(self):
        charges_line = re.findall(r'Charges : CHF [0-9\']*', self.assets)
        return self._getFirstInt(charges_line)

    def getLoyerBrut(self):
        # no example found yet, so calculate from charges + loyer
        if self.v:
            print('loyer_net', self.getLoyerNet())
            print('charges', self.getCharges())
        if self.getLoyerNet() > 0 or self.getCharges() > 0:

            return self.getLoyerNet() + self.getCharges()
        else:
            return -1

    def getListingSpace(self):
        space = re.findall(r'([0-9]+)\sm<sup', self.assets)
        return self._getFirstInt(space)

    def getDescription(self):
        # strips html tags and returns the text
        descr = self.response.css('div.im__postContent__body p')
        descr_strings = descr.css('p::text').getall()
        return ''.join(descr_strings)

    def getAddress(self):
        def addZipAndCitytoDict(addr_string):
            city_pat = '(Prilly|Renens|Ecublens|Lausanne)'
            zip_pat = '([0-9]{4})'
            zip_city = re.findall(zip_pat + r'\s' + city_pat, addr_string)
            if len(zip_city) == 0:
                address_dict['Zip'] = -1
                address_dict['City'] = ''
            else:
                address_dict['Zip'] = int(zip_city[0][0])
                address_dict['City'] = zip_city[0][1]

        def parseIncompleteAddress(address):
            addZipAndCitytoDict(address_dict, address)
            if address_dict['Zip'] == -1:
                address_dict['Street'] = address
            else:
                address_dict['Street'] = ''

        address_pat = r'big\">\s*([\w\s-]+)(<br>)*([\w\s-]+)<br>\s*<'
        matches = re.findall(address_pat, self.assets)
        address = self._getFirstString(matches)

        address_dict = {}
        if len(address) == 0:
            address_dict = self._getDefaultAddress()
        elif len(address) == 1:
            parseIncompleteAddress(address)
        else:
            address_dict['Street'] = address[0]
            addZipAndCitytoDict(address[2])

        return (address_dict)

    def getLatLong(self):
        latlong = re.findall(r'query=([0-9.]+),([0-9.]+)"', self.assets)
        return self._getFirstLatLong(latlong)

    def getReference(self):
        reference = re.findall(r'rence\s*([^<]+)\s*</span>', self.assets)
        return self._getFirstString(reference).rstrip()

    def getAnnouncer(self):
        html_text = (self.response.body).decode("utf-8")
        pat = r'<a class="link-detail-agency-url" value=["0-9]+\shref="https?://([^"]+)"\st'
        announcer = re.findall(pat, html_text)
        return self._getFirstString(announcer).rstrip()
