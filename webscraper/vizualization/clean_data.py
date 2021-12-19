import pandas as pd
import numpy as np

file_name = '/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/vizualization/cleaned_data' \
            '/realities.csv'


def calculate_price(price, area):
    if price is None or area is None:
        return None
    return price / area


def load_dataset(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def create_payment_column(data: pd.DataFrame) -> pd.DataFrame:
    data['payment'] = np.where(data.price.str.contains("vyžádání"), "unknown",
                               np.where(data.price.str.contains("měsíc"), "monthly",
                                        np.where(data.price.str.endswith("Kč"), "total",
                                                 "unknown")))
    return data


def strip_text_from_payment(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[data.payment == "unknown", "price"] = np.NAN
    data.loc[data.payment == "monthly", "price"] = data.loc[data.payment == "monthly", "price"].map(
        lambda x: x.rstrip(' Kč/měsíc'))
    data.loc[data.payment == "total", "price"] = data.loc[data.payment == "total", "price"].map(
        lambda x: x.rstrip(' Kč'))
    return data


def strip_text_from_util_area(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[data["util_area"].notnull(), "util_area"] = data.loc[data["util_area"].notnull(), "util_area"].map(
        lambda x: x.rstrip(' m'))
    return data


def make_int_from_price(data: pd.DataFrame) -> pd.DataFrame:
    data["price"] = data["price"].str.split(' ')
    data["price"] = data["price"].str.join('')
    data["price"] = data["price"].str.replace(",", ".")
    data["price"] = pd.to_numeric(data["price"])
    return data


def create_has_property_column(data: pd.DataFrame) -> pd.DataFrame:
    data["has_property"] = data["land_area"].apply(lambda x: pd.notnull(x))
    return data


def replace_nan(data: pd.DataFrame) -> pd.DataFrame:
    data["property"] = data["property"].fillna("neznámý")
    data["building_type"] = data["building_type"].fillna("neznámý")
    return data


def extract_number_of_rooms_from_title(data: pd.DataFrame) -> pd.DataFrame:
    data["title"] = data["title"].str.split("+")
    data["number_of_rooms"] = np.NaN
    for z in data.index:
        if len(data.loc[z, "title"]) >= 2:
            if data.loc[z, "title"][0][-1].isnumeric():
                data.loc[z, "number_of_rooms"] = float(data.loc[z, "title"][0][-1])
                if data.loc[z, "title"][1][0].isnumeric():
                    data.loc[z, "number_of_rooms"] += float(data.loc[z, "title"][1][0])
                if data.loc[z, "title"][1][0] == 'k':
                    data.loc[z, "number_of_rooms"] += float(0.5)

    data["title"] = data["title"].str.join(' ')
    return data


def clean_data():
    df = load_dataset('/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/webscraper/output_files'
                      '/realities.csv')
    df = create_payment_column(df)
    df = strip_text_from_payment(df)
    df = strip_text_from_util_area(df)
    df = make_int_from_price(df)
    df = create_has_property_column(df)
    df = replace_nan(df)
    df = extract_number_of_rooms_from_title(df)

    # noinspection PyTypeChecker
    df.to_csv(file_name, sep=',', mode='w')


clean_data()
# title, location, price, util_area, land_area, property, building, payment
