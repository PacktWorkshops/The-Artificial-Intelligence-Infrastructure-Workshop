import os
import sys
import pytest
import subprocess
from os import path

# change workding dir to Chapter09
os.chdir(path.dirname(path.dirname(path.abspath(__file__))))


def test_file():
    # run script
    subprocess.check_call(['python', 'Exercise01/get_trendy_vids.py'])
    assert "top_10_trendy_vids.csv" in os.listdir('Data')