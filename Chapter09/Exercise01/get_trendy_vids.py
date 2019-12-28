from pathlib import Path
import pandas as pd

def get_topn_viewed(df, date, topn):
    return df.query('trending_date==@date').sort_values('views', ascending=False).head(topn)


if __name__ == "__main__":
    print()
    PATH_FILE_IN = Path(__file__).parent.absolute()/'../Data/USvideos.csv.zip'
    PATH_FILE_OUT = Path(__file__).parent.absolute()/'../Data/top_10_trendy_vids.csv'
    DATE = "17.14.11"
    TOPN = 10

    # read data
    df_data = pd.read_csv(PATH_FILE_IN, compression='zip')
    # get top n trendy
    df_trendy = get_topn_viewed(df_data, DATE, TOPN)
    # save results
    df_trendy.to_csv(PATH_FILE_OUT, index=False)
