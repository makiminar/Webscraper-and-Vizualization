import pandas as pd
import numpy as np

df = pd.read_csv('../webscraper/output_files/realities.csv')

# print(df)

df['payment'] = np.where(df.price.str.contains("vyžádání"), "unknown",
                         np.where(df.price.str.contains("měsíc"), "monthly",
                                  np.where(df.price.str.endswith("Kč"), "total",
                                           "unknown")))

df.loc[df.payment == "unknown", "price"] = np.NAN
df.loc[df.payment == "monthly", "price"] = df.loc[df.payment == "monthly", "price"].map(lambda x: x.rstrip(' Kč/měsíc'))
df.loc[df.payment == "total", "price"] = df.loc[df.payment == "total", "price"].map(lambda x: x.rstrip(' Kč'))

print(df)

df.to_csv('./cleaned_data/realities.csv')

# title, location, price, util_area, land_area, property, building, payment
