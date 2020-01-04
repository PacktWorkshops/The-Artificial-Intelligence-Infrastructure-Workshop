import os
import sys
import pytest
import subprocess
from os import path

# change workding dir to Chapter09
os.chdir(path.dirname(path.dirname(path.abspath(__file__))))


def test_file_vids():
    # run script
    subprocess.check_call(['python', 'Exercise03/filter_data.py', '--file', 'Data/USvideos.csv.zip', '--date', '17.14.11'])
    assert "data_vids.csv" in os.listdir('Exercise03/tmp/')


def test_file_cats():
    # run script
    subprocess.check_call(['python', 'Exercise03/preprocess_data.py', '--file', 'Data/US_category_id.json'])
    assert "data_cats.csv" in os.listdir('Exercise03/tmp/')


def test_file_joined():
    # run script
    subprocess.check_call(['python', 'Exercise03/join_data.py'])
    assert "data_joined.csv" in os.listdir('Exercise03/tmp/')


def test_file_topn():
    # run script
    subprocess.check_call(['python', 'Exercise03/sort_data.py'])
    assert "data_topn.csv" in os.listdir('Exercise03/tmp/')


def test_file_output():
    # run script
    subprocess.check_call(['python', 'Exercise03/store_data.py', '--path', 'Data/top_10_trendy_cats.csv'])
    assert "top_10_trendy_cats.csv" in os.listdir('Data')