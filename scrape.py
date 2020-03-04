from scrapy.crawler import CrawlerProcess
from sas_scraper.sas_scraper.spiders.ImmobilierSpider import ImmobilierSpider
from sas_scraper.sas_scraper.spiders.ImmoscoutSpider import ImmoscoutSpider


def scrape():
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; \
                              MSIE    7.0; Windows NT 5.1)'
                              })
    process.crawl(ImmobilierSpider)
    process.crawl(ImmoscoutSpider)
    process.start()


if __name__ == '__main__':
    runner = CrawlerProcess()
    scrape()
