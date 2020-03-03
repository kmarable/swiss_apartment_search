import pandas as import pd
from src.utilities.dataFile import DataFile
from src.location import M1Line
from src.config import conf


def remove_duplicates(df):
    #basically want to pivot a few columsn
    df.pivot(index=['Announcer', 'Reference'], columns='host', values='id')

def process():
    raw_file = conf['DEFAULT']['raw_file']
    raw_data = pd.read_csv()

    no_duplicates = raw_data.remove_duplicates()
    latlong = zip(df['Latitude'], df['Longitude'])
    coord_list = [(x, y) for x, y in latlong]
    line = M1Line()
    new_df = line.getDFofNearestStops(coord_list)
    print(new_df)
    processed_apartments = df.join(new_df)
    print('processed_apartments', processed_apartments['NearestStop'])
    processed_apartments.to_csv('data\\processed.csv')


if __name__ == '__main__':
    process()
