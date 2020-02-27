from scrapy.crawler import CrawlerProcess
from update import  update_raw
from sas_scraper.sas_scraper.spiders.apartment_spider import ApartmentSpider

if __name__ == '__main__':
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; \
                              MSIE    7.0; Windows NT 5.1)'
                              })
    process.crawl(ApartmentSpider)
    process.start()

    print('spider finished')
    update_raw()
