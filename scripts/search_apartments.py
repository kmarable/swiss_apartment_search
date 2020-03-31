import set_env_variables  # noqa

from scripts.scrape import scrape
from scripts.process import process
from scripts.update import update_raw
from scripts.report import generate_report

if __name__ == '__main__':
    scrape()
    update_raw()
    process()
    generate_report()
