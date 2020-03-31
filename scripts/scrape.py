import os
import set_env_variables  # noqa
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from sas_scraper.sas_scraper.spiders.ImmobilierSpider import ImmobilierSpider
from sas_scraper.sas_scraper.spiders.ImmoscoutSpider import ImmoscoutSpider


def scrape():

    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'sas_scraper.sas_scraper.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')

    process = CrawlerProcess(settings)
    process.crawl(ImmobilierSpider)
    process.crawl(ImmoscoutSpider)
    process.start()


if __name__ == '__main__':
    runner = CrawlerProcess()
    scrape()
