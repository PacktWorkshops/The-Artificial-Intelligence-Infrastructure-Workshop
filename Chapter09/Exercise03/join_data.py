import pandas as pd

def join_cats(df_vids, df_cats):
    return df_vids.merge(df_cats, left_on='category_id', right_on='id')

if __name__ == "__main__":
    import os
    import sys
    from os import path
    # read data from cache
    try:
        df_vids = pd.read_csv('./tmp/data_vids.csv')
        df_cats = pd.read_csv('./tmp/data_cats.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)

    # join data
    df_join = join_cats(df_vids, df_cats)

    # cache joined data
    df_join.to_csv('./tmp/data_joined.csv')
    print('[ data pipeline ] finish join data')