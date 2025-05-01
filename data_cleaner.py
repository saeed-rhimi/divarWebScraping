import numpy as np
import pandas as pd


class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()

    def clean_data(self):
        self.df = self.df[
            self.df["Total Price"].str.contains("تومان") & self.df["Price per Meter"].str.contains("تومان")]
        self.df = self.df[self.df["Build Year"].str.isnumeric()]
        self.df = self.df[self.df['Room Count'].str.isdigit()]
        self.df.loc[:, 'Total Price'] = self.df['Total Price'].str.replace('تومان', '', regex=False)
        self.df.loc[:, 'Total Price'] = self.df['Total Price'].str.replace('٬', '', regex=False)
        self.df.loc[:, 'Total Price'] = self.df['Total Price'].astype(float)
        self.df.loc[:, 'Price per Meter'] = self.df['Price per Meter'].str.replace('تومان', '', regex=False)
        self.df.loc[:, 'Price per Meter'] = self.df['Price per Meter'].str.replace('٬', '', regex=False)
        self.df.loc[:, 'Price per Meter'] = self.df['Price per Meter'].astype(float)
        self.df.loc[:, ['Floor Number', 'Total Floors']] = self.df.loc[:, ['Floor Number', 'Total Floors']].replace(
            "Not Found", np.nan)
        self.df.loc[:, 'Room Count'] = self.df['Room Count'].astype(str).str.replace("+4", "5")
        string_columns = ['Title', 'Description', 'Characteristics', 'Features', 'URL']
        self.df.loc[:, string_columns] = self.df.loc[:, string_columns].astype(pd.StringDtype())
        self.df.loc[:, "Crawl Date"] = pd.to_datetime(self.df["Crawl Date"], errors="coerce").dt.date
        self.df.loc[:, 'Property Size'] = pd.to_numeric(self.df['Property Size'], errors='coerce').astype('Int64')
        self.df.loc[:, 'Build Year'] = pd.to_numeric(self.df['Build Year'], errors='coerce').astype('Int32')
        self.df.loc[:, 'Total Price'] = pd.to_numeric(self.df['Total Price'], errors='coerce').astype(float)
        self.df.loc[:, 'Price per Meter'] = pd.to_numeric(self.df['Price per Meter'], errors='coerce').astype(float)
        self.df.loc[:, 'Room Count'] = pd.to_numeric(self.df['Room Count'], errors='coerce').astype('Int64')
        self.df.loc[:, 'Floor Number'] = pd.to_numeric(self.df['Floor Number'], errors='coerce').astype('Int64')
        self.df.loc[:, 'Total Floors'] = pd.to_numeric(self.df['Total Floors'], errors='coerce').astype('Int64')
        return self.df
