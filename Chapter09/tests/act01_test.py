import os
import sys
import json
import shutil
import pytest
from datetime import datetime
from os import path
from airflow import DAG
import pandas as pd
from airflow.operators.python_operator import PythonOperator
from airflow.models import TaskInstance
# change workding dir to Chapter09
os.chdir(path.dirname(path.dirname(path.abspath(__file__))))

def filter_data(**kwargs):
    # read data
    path_vids = kwargs['path_vids']
    date = str(kwargs['date'])

    print(os.getcwd())
    print(path_vids)

    df_vids = pd.read_csv(path_vids, compression='zip') \
        .query('trending_date==@date')
    # cache
    try:
        df_vids.to_csv('./tmp/data_vids.csv', index=False)
    except FileNotFoundError:
        os.mkdir('./tmp')
        df_vids.to_csv('./tmp/data_vids.csv', index=False)
    return

def preprocess_data(**kwargs):
    # read data
    path_cats = kwargs['path_cats']
    data_cats = json.load(open(path_cats, 'r'))
    # convert json to dataframe
    df_cat = pd.DataFrame(data_cats)
    df_cat['category'] = df_cat['items'].apply(lambda x: x['snippet']['title'])
    df_cat['id'] = df_cat['items'].apply(lambda x: int(x['id']))
    df_cat_drop = df_cat.drop(columns=['kind', 'etag', 'items'])
    # cache
    try:
        df_cat_drop.to_csv('./tmp/data_cats.csv')
    except FileNotFoundError:
        os.mkdir('./tmp')
        df_cat_drop.to_csv('./tmp/data_cats.csv')


def join_data(**kwargs):
    try:
        df_vids = pd.read_csv('./tmp/data_vids.csv')
        df_cats = pd.read_csv('./tmp/data_cats.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)
    # join data
    df_join = df_vids.merge(df_cats, left_on='category_id', right_on='id')
    # cache joined data
    df_join.to_csv('./tmp/data_joined.csv')


def calc_ratio(**kwargs):
    try:
        df_join = pd.read_csv('./tmp/data_joined.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)
    # aggreate likes and dislikes by category
    df_agg = df_join[['category', 'likes', 'dislikes']].groupby('category').sum()
    # calculate ratio
    df_agg['ratio_likes_dislikes'] = df_agg['likes'] / df_agg['dislikes']
    df_agg.reset_index('category').to_csv('./tmp/data_ratio.csv', index=False)


def sort_data(**kwargs):
    try:
        df_ratio = pd.read_csv('./tmp/data_ratio.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)
    # sort data
    df_sorted = df_ratio.sort_values('ratio_likes_dislikes', ascending=False)
    # cache joined data
    df_sorted.to_csv('./tmp/data_sorted.csv', index=False)


def store_data(**kwargs):
    # read data from cache
    path_output = kwargs['path_output']
    try:
        df_join = pd.read_csv('./tmp/data_sorted.csv')
    except Exception as e:
        print('>>>>>>>>>>>> Error: {}'.format(e))
        sys.exit(1)
    # cache joined data
    df_join.to_csv(path_output)
    # clean up tmr
    shutil.rmtree('./tmp')


@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={"owner": "airflow", "start_date": datetime(2017, 11, 14)},
    )


def test_filter_data(test_dag):
    task = PythonOperator(
        task_id='filter_data',
        python_callable=filter_data,
        op_kwargs={'path_vids': 'Data/USvideos.csv.zip', 'date': '17.14.11'},
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "data_vids.csv" in os.listdir('tmp')


def test_preprocess_data(test_dag):
    task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        op_kwargs={'path_cats': 'Data/US_category_id.json'},
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "data_cats.csv" in os.listdir('tmp')


def test_join_data(test_dag):
    task = PythonOperator(
        task_id='join_data',
        python_callable=join_data,
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "data_joined.csv" in os.listdir('tmp')


def test_calc_ratio(test_dag):
    task = PythonOperator(
        task_id='calc_ratio',
        python_callable=calc_ratio,
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "data_ratio.csv" in os.listdir('tmp')


def test_sort_data(test_dag):
    task = PythonOperator(
        task_id='sort_data',
        python_callable=sort_data,
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "data_sorted.csv" in os.listdir('tmp')


def test_store_data(test_dag):
    task = PythonOperator(
        task_id='store_data',
        python_callable=store_data,
        op_kwargs={'path_output': 'Data/Ratio_Likes_Dislikes.csv'},
        dag=test_dag)
    test_dag.clear()
    ti = TaskInstance(task=task, execution_date=datetime.now())
    task.execute(ti.get_template_context())
    assert "Ratio_Likes_Dislikes.csv" in os.listdir('Data')