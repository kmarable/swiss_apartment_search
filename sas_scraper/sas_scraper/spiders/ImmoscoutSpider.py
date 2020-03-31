import re
from sas_scraper.sas_scraper.spiders import ApartmentSpider


class ImmoscoutSpider(ApartmentSpider):
    name = "Immoscout"

    def getHost(self):
        return 'Immoscout'

    def getUrls(self):
        urls = [
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-renens-vd',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-prilly',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-ecublens-vd',
            'https://www.immoscout24.ch/fr/immobilier/louer/lieu-lausanne'
        ]
        return urls

    def getListings(self, response):
        return response.css('article')

    def getPageScript(self, response):
        state = response.css("script[id^='state']").get()
        return state

    def pageIsLast(self, response):
        pageData = self.getPageScript(response)
        currentPage = re.findall('"currentPage":([0-9]+)', pageData)[0]
        totalPages = re.findall('"totalPages":([0-9]+)', pageData)[0]

        is_last = False
        if currentPage == totalPages:
            is_last = True
        return is_last

        self.logger.debug('total pages %s' % totalPages)
        self.logger.debug('current pages %s' % currentPage)

    def getNextPage(self, url):
        self.logger.debug('searching url %s' % url)

        url_components = re.search('(.*pn=)([0-9]+)', url)
        if url_components:
            page_num = url_components.group(2)
            self.logger.debug('pagenum %s' % page_num)
            new_page_num = int(page_num) + 1
            new_url = url_components.group(0) + str(new_page_num)
        else:
            new_url = url + '?pn=2'

        self.logger.debug('next page url %s' % new_url)

        return new_url

    def getListingLink(self, listing):
        link = listing.css("article a").attrib['href']
        return link

    def getListingID(self, listing):
        link = self.getListingLink(listing)
        id_num = re.findall(r'/([0-9]+)\?s', link)

        self.logger.debug('listing id is %s' % str(id_num))

        if len(id_num) > 0:
            return int(id_num[0])
        else:
            return -1
