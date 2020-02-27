import os
import re
import pandas as pd
from datetime import date
from src.utilities.htmlFile import htmlFile


class ApartmentSpider(scrapy.Spider):
    name = "Apartment"
    filename_root = "data\\immobilier_pages\\"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='ApartmentSpiderLog.txt',
        format='%(levelname)s: %(message)s',
        level=logging.DEBUG
    )

    def __init__(self, category=None, *args, **kwargs):
        super(ApartmentSpider, self).__init__(*args, **kwargs)
        self.old_ids = load_old_ids('data\\raw_data.csv')
        self.log('loading old ids')
        for id in self.old_ids:
            self.log('found old id %i' % id)

    def start_requests(self):
        urls = [
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/renens/page-1?t=rent&c=1;2&p=c12292&nb=false',
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/lausanne/page-1?t=rent&c=1;2&p=c11115&nb=false&gr=1',
            'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/ecublens/page-1?t=rent&c=1;2&p=c10033&nb=false&gr=1', 'https://www.immobilier.ch/fr/carte/louer/appartement-maison/vaud/prilly/page-1?t=rent&c=1;2&p=c12211&nb=false&gr=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseMain)

    def save_main_page(self, response):
        filename = os.path.join(ApartmentSpider.filename_root, 'test_page.html')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def pageIsLast(self, response):
        items_on_page = response.css("div.items-result-count").get()
        results = re.search('([0-9]+) / ([0-9]+)', items_on_page)
        if results.group(1) == results.group(2):
            return True
        else:
            return False

    def getNextPage(self, url):
        result = re.findall('(.*page-)([0-9]+)(\?.*)', url)
        if len(result) > 0:
            address_components = result[0]
            page_num = address_components[1]
            new_page_num = int(page_num) + 1
            new_address = address_components[0] + str(new_page_num) + address_components[2]
            return(new_address)
        else:
            print('bad address format')
            return None

    def parseMain(self, response):
        self.log('parsing page ')
        listings = response.css('div.filter-item-container')
        self.log('found %i listings ' % len(listings))

        if not self.pageIsLast(response):
            next_page = self.getNextPage(response.url)
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parseMain)

        n_max = 100
        i  = 0
        for l in listings:
            id = get_listing_id(l)
            self.log('found id %i' % id)
            if i > n_max:
                return
            elif (id in self.old_ids):
                continue  # go on to next link
            else:
                print('NEW??', i, id, self.old_ids, id in self.old_ids)
                i = i+1
                link = getListingLink(l)
                self.log('sending request for %s' % link)
                full_link = response.urljoin(link)
                request = scrapy.Request(full_link, callback=self.savePage)
                request.meta['id'] = id
                yield request


    def savePage(self, response):
        id = response.meta['id']
        file_name = self.getListingFileName(id)
        save_file = htmlFile(file_name)
        self.log('in savePage %s' % save_file.path)
        # make header_dict
        header_dict = {}
        header_dict['link'] = response.url
        header_dict['id'] = id
        header_dict['host'] = 'Immobilier'
        header_dict['date'] = str(date.today())
        save_file.write(response.text, header_dict)
        self.log('Saved file %s' % file_name)

    def getListingFileName(self, id):
        today = str(date.today())

        file_name = os.path.join(ApartmentSpider.filename_root,
                                 today + '_' + str(id) + '.html')
        return file_name


def getListingLink(listing):
    link = listing.css("a[id^='link-result-item']::attr(href)").get()
    return link


def get_listing_id(listing):
    id = listing.css("a[id^='link-result-item']::attr(id)").get()
    if id is None:
        return -1
    id_num = re.findall('[0-9]+', id)
    if len(id_num) > 0:
        return int(id_num[0])
    else:
        return -1


def load_old_ids(file_name):
    if not os.path.exists(file_name):
        return []
    else:
        old_data = pd.read_csv(file_name)
        old_immobilier = old_data[old_data['host'] == 'Immobilier\n']
        old_ids = [int(id) for id in old_immobilier['id']]
        return list(old_ids)
