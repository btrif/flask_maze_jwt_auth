#  Created by btrif Trif on 13-07-2022 , 2:55 PM.
import time

import pytest

import routes
from tools import MazeGrid
from routes import hello





def test_maze_id_solution():
    assert 1 == 1


# def test_hello(self):
#
#     print(f"request_mock    {}")


def sleep_awhile(duration):
    """sleep for couple of seconds"""
    time.sleep(duration)
    # some other processing steps

def test_sleep_awhile(mocker):
    m = mocker.patch("time.sleep", return_value=None)
    sleep_awhile(3)
    m.assert_called_once_with(3)
    m.assert_called()

