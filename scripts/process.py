import set_env_variables  # noqa: F401
import pandas as pd
from src.location import M1Line
from src.config import conf


def process():
    print('processing....')
    # load data
    raw_file = conf['DEFAULT']['raw_file']
    raw_data = pd.read_csv(raw_file)
    print(raw_data.shape, 'listings in raw file')

    # remove duplicate data
    df = remove_duplicates(raw_data)
    print(df.shape, 'listings with duplicates removed')

    # other processing
    df = add_M1_distance(df)

    # write processed data to file
    print('final df', df.shape)
    df.to_csv('data\\processed.csv')


def remove_duplicates(df):
    df = df.drop_duplicates(['Announcer', 'Reference'], keep='first')
    return df


def add_M1_distance(df):
    latlong = zip(df.index, df['Latitude'], df['Longitude'])
    coord_list = [z for z in latlong]
    line = M1Line()
    new_df = line.getDFofNearestStops(coord_list)
    processed_apartments = df.join(new_df)
    return processed_apartments


if __name__ == '__main__':
    process()
