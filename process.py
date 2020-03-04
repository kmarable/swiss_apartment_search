import pandas as pd
from src.location import M1Line
from src.config import conf
from datetime import datetime as dt


def mark_old(df):
    # flags listings that were in a previous report (i.e. already looked at)
    old_results = conf['DEFAULT']['old_results']
    old_df = pd.read_csv(old_results)
    old_ids = df['id'].isin(old_df['id'])
    old_host = [h == 'Immobilier' for h in df['host']]
    df['old'] = [id and h for id, h in zip(old_ids, old_host)]
    print('number of old listings:', df['old'].value_counts())
    return df


def remove_duplicates(df):
    df = df.drop_duplicates(['Announcer', 'Reference'], keep='first')
    return df


def correct_availability(df):
    df2 = df.copy()
    df2['adate'] = [dt.strptime(d, '%Y-%m-%d') for d in df['Availability']]

    def correct(availability, date):
        if availability == dt(1970, 1, 1):
            # default indicating not found or 'toute de suite'
            return date  # return date listing was downloaded
        else:
            return availability
    date_itr = zip(df2['adate'], df2['date'])
    df2['Availability'] = [correct(a, d) for a, d in date_itr]
    return df2


def process():
    print('processing....')
    raw_file = conf['DEFAULT']['raw_file']
    raw_data = pd.read_csv(raw_file)
    print(raw_data.shape, 'listings in raw file')
    df = remove_duplicates(raw_data)
    print(df.shape, 'listings with duplicates removed')
    df = mark_old(df.copy())
    df = correct_availability(df)
    latlong = zip(df.index, df['Latitude'], df['Longitude'])
    coord_list = [z for z in latlong]
    line = M1Line()
    new_df = line.getDFofNearestStops(coord_list)
    processed_apartments = df.join(new_df)
    print('final df', processed_apartments.shape)
    processed_apartments.to_csv('data\\processed.csv')


if __name__ == '__main__':
    process()
