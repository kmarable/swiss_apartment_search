import re
from sas_scraper.sas_scraper.spiders import ApartmentSpider


class ImmoscoutSpider(ApartmentSpider):
    name = "Immoscout"

    def getSite(self):
        return 'Immoscout'

    def getUrls(self):
        urls = [
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-renens-vd',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-prilly',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-ecublens',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-lausanne'
        ]
        return urls

    def getListings(self, response):
        return response.css('article')

    def getScript(self, response):
        state = response.css("script[id^='state']").get()
        return state

    def pageIsLast(self, response):
        pageData = self.getScript(response)
        currentPage = re.findall('"currentPage":([0-9]+)', pageData)[0]
        totalPages = re.findall('"totalPages":([0-9]+)', pageData)[0]
        if currentPage == totalPages:
            return True
        else:
            return False

    def getNextPage(self, url):
        result = re.findall('(.*pn=)([0-9]+)', url)
        if len(result) > 0:
            address_components = result[0]
            page_num = address_components[1]
            new_page_num = int(page_num) + 1
            new_address = address_components[0] + str(new_page_num)
            return(new_address)
        else:
            print('bad address format')
            return None

    def getListingLink(self, listing):
        link = listing.css("article a").attrib['href']
        return link

    def getListingID(self, listing):
        link = self.getListingLink(listing)
        print('the link', link)
        id_num = re.findall('/([0-9]+)\?s', link)
        print('INT', id_num)
        if len(id_num) > 0:
            return int(id_num[0])
        else:
            return -1
