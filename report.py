import pandas as pd
from datetime import datetime as dt


def get_availability_mask(df):
    df['adate'] = [dt.strptime(d, '%Y-%m-%d') for d in df['Availability']]
    avail_filter = df['adate'] < dt(2020, 6, 1)
    return avail_filter


def generate_report():
    df = pd.read_csv('data\\processed.csv')

    chambre_filter = df['chambre'] >= 2
    area_filter = df['ListingSpace'] > 60
    price_filter = df['LoyerBrut'] < 2400
    loc_filter = df['TimeToNearestStop'] < 10
    avail_filter = get_availability_mask(df)

    filtered_apartments = df[area_filter & price_filter & loc_filter
                             & chambre_filter & avail_filter]

    report_columns = ['old', 'link', 'Announcer', 'Availability',
                      'ListingSpace', 'LoyerNet', 'Charges',
                      'LoyerBrut', 'Street', 'Zip', 'City',
                      'Latitude', 'Longitude', 'NearestStop',
                      'TimeToNearestStop']

    df_view = filtered_apartments[report_columns]
    df_view.to_csv('report.csv')
    print(df_view.shape, 'apartments meeting criteria')


if __name__ == '__main__':
    generate_report()
