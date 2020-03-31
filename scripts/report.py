import set_env_variables  # noqa
import pandas as pd
from datetime import datetime as dt


def generate_report():
    # read data
    df = pd.read_csv('data\\processed.csv')

    # Criteria to filter on
    chambre_filter = df['chambre'] >= 2
    area_filter = df['ListingSpace'] > 60
    price_filter = df['LoyerBrut'] < 2400
    loc_filter = df['TimeToNearestStop'] < 10
    avail_filter = get_availability_mask(df)

    # apply filter
    filtered_apartments = df[area_filter & price_filter & loc_filter
                             & chambre_filter & avail_filter]

    report_columns = ['link', 'Announcer', 'Availability',
                      'ListingSpace', 'LoyerNet', 'Charges',
                      'LoyerBrut', 'Street', 'Zip', 'City',
                      'Latitude', 'Longitude', 'NearestStop',
                      'TimeToNearestStop']

    # keep only desired report_columns
    df_view = filtered_apartments[report_columns]

    # write filtered data to a report file
    df_view.to_csv('data\\report.csv')
    print(df_view.shape, 'apartments meeting criteria')


def get_availability_mask(df):
    df['adate'] = [dt.strptime(d, '%Y-%m-%d') for d in df['Availability']]
    avail_filter = df['adate'] < dt(2020, 6, 1)
    return avail_filter


if __name__ == '__main__':
    generate_report()
