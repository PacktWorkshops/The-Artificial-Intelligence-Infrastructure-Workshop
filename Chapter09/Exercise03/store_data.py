import sys
import shutil
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="exercise 3",
        description="store data")
    parser.add_argument('-p', '--path', type=str, required=True, help='file path to persist final data')
    return parser.parse_args()

if __name__ == "__main__":
    from pathlib import Path
    # get args
    args = parse_args()
    filepath = args.path

    # read data from cache
    try:
        file_cached = './tmp/data_topn.csv'
        df_join = pd.read_csv(file_cached)
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)

    # cache joined data
    df_join.to_csv(filepath, index=False)

    # clean up tmp
    shutil.rmtree('./tmp')

    print('[ data pipeline ] finish storing data')