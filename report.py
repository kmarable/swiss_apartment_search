import pandas as pd


def generate_report():
    df = pd.read_csv('data\\processed.csv')

    chambre_filter = df['chambre'] >= 2
    area_filter = df['Space'] > 60
    price_filter = df['TotalRent'] < 2400
    loc_filter = df['TimeToNearestStop'] < 10

    filtered_apartments = df[area_filter & price_filter & loc_filter & chambre_filter]

    filtered_apartments.to_csv('report.csv')


if __name__ == '__main__':
    generate_report()
