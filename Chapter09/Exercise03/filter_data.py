import argparse
import os
from pathlib import Path
import pandas as pd


def filter_by_date(df, date):
    return df.query('trending_date==@date')


def parse_args():
    parser = argparse.ArgumentParser(
        prog="exercise 3",
        description="filter data by date")
    parser.add_argument('-f', '--file', type=str, required=True, help='source data file path')
    parser.add_argument('-d', '--date', type=str, required=True, help='date format yy.dd.mm')
    return parser.parse_args()


if __name__ == "__main__":
    # get args
    args = parse_args()
    filepath = args.file
    date = args.date

    # read data
    df_data = pd.read_csv(filepath, compression='zip')
    # filter
    df_filtered = filter_by_date(df_data, date)
    # cache
    dir_cache = Path(__file__).parent.absolute()/'tmp'
    try:
        df_filtered.to_csv(os.path.join(dir_cache, 'data_vids.csv'), index=False)
    except FileNotFoundError:
        os.mkdir(dir_cache)
        df_filtered.to_csv(os.path.join(dir_cache, 'data_vids.csv'), index=False)
    print('[ data pipeline ] finish filter data')
