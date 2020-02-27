from src.parser.ImmobilierParser import ImmobilierParser


def update_raw():
    parser = ImmobilierParser()

    parser.extractAll()


if __name__ == '__main__':
    update_raw()
