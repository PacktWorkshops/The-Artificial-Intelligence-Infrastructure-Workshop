import json
from pathlib import Path

import pandas as pd


def get_topn_categories(df, date, topn):
    return df.query('trending_date==@date') \
        .groupby('category')[['views']].sum() \
        .sort_values('views', ascending=False).head(topn)


if __name__ == "__main__":
    # config
    PATH_FILE_VIDS = Path(__file__).parent.absolute()/'../Data/USvideos.csv.zip'
    PATH_FILE_CAT = Path(__file__).parent.absolute()/'../Data/US_category_id.json'
    PATH_FILE_OUT = Path(__file__).parent.absolute()/'../Data/top_10_trendy_cats.csv'
    DATE = "17.14.11"
    TOPN = 10

    # read data
    df_vids = pd.read_csv(PATH_FILE_VIDS, compression='zip')
    data_cats = json.load(open(PATH_FILE_CAT , 'r'))
    # convert json to dataframe
    df_cat = pd.DataFrame(data_cats)
    df_cat['category'] = df_cat['items'].apply(lambda x: x['snippet']['title'])
    df_cat['id'] = df_cat['items'].apply(lambda x: int(x['id']))
    df_cat_drop = df_cat.drop(columns=['kind', 'etag', 'items'])
    # join cat with source data
    df_join = df_vids.merge(df_cat_drop, left_on='category_id', right_on='id')
    # get top10 cats
    df_trendy = get_topn_categories(df_join, DATE, TOPN)
    # save results
    df_trendy.to_csv(PATH_FILE_OUT)
