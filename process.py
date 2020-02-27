from src.utilities.dataFile import DataFile
from src.location import M1Line


def process():
    raw_data = DataFile()

    df = raw_data.read_file()

    df['TotalRent'] = df['LoyerNet'] + df['Charges']

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
