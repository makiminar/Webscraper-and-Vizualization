# -*- coding: utf-8 -*-
import os

import pytest
import pandas as pd
import numpy as np
from webscraper.vizualization.clean_data import load_dataset, calculate_price, create_payment_column, \
    strip_text_from_payment, strip_text_from_util_area, make_int_from_price, create_has_property_column, replace_nan, \
    extract_number_of_rooms_from_title, clean_data

data_dir = '/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/webscraper/output_files/'


def test_exists():
    """checks if the file file exists in the correct repository"""
    assert os.path.isfile('/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/vizualization'
                          '/clean_data.py')


def test_load_dataset():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    assert (isinstance(df, pd.DataFrame))
    assert (df.shape[1] == 10)
    assert (df.shape[0] > 0)


def test_calculate_price():
    price = 50000
    area = 64
    assert (price / area) == calculate_price(price, area)
    assert None == calculate_price(None, area)
    assert None == calculate_price(price, None)


def test_create_payment_column():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = create_payment_column(df)
    assert set(df["payment"].unique()) == {"unknown", "monthly", "total"}


def test_strip_text_from_payment():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = create_payment_column(df)
    df = strip_text_from_payment(df)
    assert df.price.str.contains(" Kč/měsíc").sum() == 0
    assert df.price.str.contains(" Kč").sum() == 0


def test_strip_text_from_util_area():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = strip_text_from_util_area(df)
    assert df.price.str.contains(" m").sum() == 0


def test_make_int_from_price():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = create_payment_column(df)
    df = strip_text_from_payment(df)
    df = make_int_from_price(df)
    assert df.price.dtype == float


def test_create_has_property_column():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = create_has_property_column(df)
    assert ("has_property" in set(df.columns)) == True


def test_replace_nan():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = replace_nan(df)
    assert df["property"].isna().sum() == 0
    assert df["building_type"].isna().sum() == 0


def test_extract_number_of_rooms_from_title():
    df = load_dataset(os.path.join(data_dir, 'realities.csv'))
    df = extract_number_of_rooms_from_title(df)
    assert ("number_of_rooms" in set(df.columns)) == True
    assert df["number_of_rooms"].dtype == float


def test_clean_data():
    clean_data()
    assert os.path.isfile('/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/vizualization'
                          '/cleaned_data/realities.csv')
