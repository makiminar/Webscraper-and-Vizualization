# -*- coding: utf-8 -*-

import os
import pytest


def test_exists():
    """checks if the file file exists in the correct repository"""
    assert os.path.isfile('/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/vizualization/app.py')
