import sys
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="exercise 3",
        description="store data")
    parser.add_argument('-p', '--path', type=str, required=True, help='file path to persist final data')
    return parser.parse_args()

if __name__ == "__main__":
    # get args
    args = parse_args()
    filepath = args.path

    # read data from cache
    try:
        df_join = pd.read_csv('./tmp/data_topn.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)

    # cache joined data
    df_join.to_csv(filepath)
