from scrapy.crawler import CrawlerProcess
from sas_scraper.sas_scraper.spiders.ImmobilierSpider import ImmobilierSpider
from sas_scraper.sas_scraper.spiders.ImmoscoutSpider import ImmoscoutSpider



def start_spider(class_name):
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; \
                              MSIE    7.0; Windows NT 5.1)'
                              })
    process.crawl(class_name)
    process.start()


def scrape():
    #start_spider(ImmobilierSpider)
    start_spider(ImmoscoutSpider)


if __name__ == '__main__':
    runner = CrawlerProcess()
    scrape()
