import os
import sys
import pytest
import subprocess
from os import path

# change workding dir to Chapter09
os.chdir(path.dirname(path.dirname(path.abspath(__file__))))


def test_file():
    # run script
    subprocess.check_call(['python', 'Exercise02/get_trendy_cats.py'])
    assert "top_10_trendy_cats.csv" in os.listdir('Data')