'''
Hi first time documenting.
This program pulls stock pricing data from yahoo finance with a period of 1 year and applies a
cleaning method to it. This method removes price percentage changes with a z-score above 3
to remove outliers. Removed dates are then interpolated and 20 and 50 day moving averages
are applied. Finally, the data is visualized with removed outliers indicated on the graph
and in the terminal. 
'''

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Stock:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self.data = None

    def _load(self):
        if self.data is None:
            self.data = self.ticker.info
        return self.data

    def name(self):
        return self._load().get("displayName")

    def get_price_history(self, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        history = self.ticker.history(period=period, interval=interval)
        if history.empty:
            raise ValueError(f"No price history data available for {self.symbol}.")
        return history
    def clean_price_data(self):
        history = self.get_price_history()
        price_history = history["Close"]
        percent_change = history["Close"].pct_change().dropna()

        std_avg = percent_change.std()
        z_scores = percent_change / std_avg
        mask = abs(z_scores) > 3 

        outlier_dates = mask[mask].index
        outlier_price = price_history[outlier_dates]
        outlier_pct = percent_change[outlier_dates]
        volatile_z_scores = z_scores[mask]

        cleaned_price = price_history.copy()
        cleaned_price.loc[outlier_dates] = np.nan
        interpolated_price = cleaned_price.interpolate(method= "linear")

        if len(outlier_dates) > 0:
            print("Outlier dates removed.")
            for date in outlier_dates:
                print(f"{date.date()}: {outlier_pct[date]:.2%} (Z-Score: {volatile_z_scores[date]:.2f})")


        ma20 = interpolated_price.rolling(window=20).mean()
        ma50 = interpolated_price.rolling(window=50).mean()

        plt.plot(ma20.index, ma20.values, label="20D MA")
        plt.plot(ma50.index, ma50.values, label="50D MA")
        plt.plot(price_history.index, price_history.values, label = "MP")
        plt.scatter(outlier_dates, outlier_price, label = "Outlier")
        plt.xlabel("2 Month Periods")
        plt.ylabel("Price $")
        plt.legend()
        plt.title(self.name() + " Stock in Past Fiscal Year")
        plt.show()
        
     
def main():
    print("Stock 1Y Visualizer")
    print("Please enter a ticker symbol")

    while True:
        symbol = input("Ticker: ").strip()
        if symbol.lower() == "exit":
            break
        try:
            stock = Stock(symbol)
            print()
            stock.clean_price_data()
            print()
        except Exception as exc:
            print(f"Error fetching data for {symbol}: {exc}")
            

main()
