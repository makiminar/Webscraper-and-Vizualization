import pandas as pd
import numpy as np


def calculate_price(price, area):
    if price is None or area is None:
        return None
    return price / area


df = pd.read_csv('../webscraper/output_files/realities.csv')

df['payment'] = np.where(df.price.str.contains("vyžádání"), "unknown",
                         np.where(df.price.str.contains("měsíc"), "monthly",
                                  np.where(df.price.str.endswith("Kč"), "total",
                                           "unknown")))

df.loc[df.payment == "unknown", "price"] = np.NAN
df.loc[df.payment == "monthly", "price"] = df.loc[df.payment == "monthly", "price"].map(lambda x: x.rstrip(' Kč/měsíc'))
df.loc[df.payment == "total", "price"] = df.loc[df.payment == "total", "price"].map(lambda x: x.rstrip(' Kč'))

df.loc[df["util_area"].notnull(), "util_area"] = df.loc[df["util_area"].notnull(), "util_area"].map(
    lambda x: x.rstrip(' m'))

df["price"] = df["price"].str.split(' ')
df["price"] = df["price"].str.join('')
df["price"] = df["price"].str.replace(",", ".")

df["has_property"] = df["land_area"].apply(lambda x: pd.notnull(x))

df["property"] = df["property"].replace(np.NaN, "neznámý")
df["building_type"] = df["building_type"].replace(np.NaN, "neznámý")

df["title"] = df["title"].str.split("+")
df["number_of_rooms"] = np.NaN

# extrahování informace o počtu místností ze sloupce 'title'
for z in df.index:
    if len(df.loc[z, "title"]) >= 2:
        if df.loc[z, "title"][0][-1].isnumeric():
            df.loc[z, "number_of_rooms"] = float(df.loc[z, "title"][0][-1])
            if df.loc[z, "title"][1][0].isnumeric():
                df.loc[z, "number_of_rooms"] += float(df.loc[z, "title"][1][0])
            if df.loc[z, "title"][1][0] == 'k':
                df.loc[z, "number_of_rooms"] += float(0.5)

df["title"] = df["title"].str.join(' ')

print(df)
df.to_csv('./cleaned_data/realities.csv')

# title, location, price, util_area, land_area, property, building, payment
