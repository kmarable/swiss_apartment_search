import configparser
from src.utilities import get_absolute_path

conf = configparser.ConfigParser()

conf.read(get_absolute_path('config.ini'))
