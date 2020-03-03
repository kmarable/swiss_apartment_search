from src.parser.ListingParser import ListingParser


def update_raw():
    parser = ListingParser()
    parser.extractAll()


if __name__ == '__main__':
    update_raw()
