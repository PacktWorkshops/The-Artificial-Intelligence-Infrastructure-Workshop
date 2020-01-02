import sys
import pandas as pd
import argparse

def get_topn_cats(df_join, topn):
    return df_join.groupby('category')[['views']].sum() \
        .sort_values('views', ascending=False).head(topn)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="exercise 3",
        description="rank categories")
    parser.add_argument('-n', '--num', type=int, default=10, help='how many?')
    return parser.parse_args()

if __name__ == "__main__":
    # get args
    args = parse_args()
    topn = args.num

    # read data from cache
    try:
        df_join = pd.read_csv('./tmp/data_joined.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)

    # sort data
    df_topn = get_topn_cats(df_join, topn)

    # cache joined data
    df_topn.to_csv('./tmp/data_topn.csv')
