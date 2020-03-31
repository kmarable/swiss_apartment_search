import set_env_variables  # noqa
from src.parser.Parser import Parser  # noqa


def update_raw():
    parser = Parser()
    parser.extractAll()


if __name__ == '__main__':
    update_raw()
