'''
First trading program :)
The rules are pretty simple and straightfoward. 
No buying if volatility is too large. This is measured by the bandwidth between upper and lower
bollinger bands being 2 standard deviations away from the moving mean with a window of 20 days.
Buy if price crosses an rsi of 30 with upwards momentum and price is within 2% proximity to 
the lower bollinger band. 
Sell if price crosses an rsi of 70 with downards momentum and price is within 2% proximity to
the upper bollinger band. 

Reused technical indicator methods from the technical indicator library.

Can visualize the signals overlayed over the price with options to overlay bollinger bands
and a seperate rsi graph.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

class Signal():
    def __init__(self, close_prices):
        self.close = pd.Series(close_prices)

    def bollingerband(self):
            bb_output = {}
    
            dates = self.close.index
            prices = self.close.values
    
            upper_b = {}
            lower_b = {}
            
            middle_b = self.close.rolling(window=20).mean()
            
            std_ = {}
    
            for i in range(0, 19):
                std_[i] = None
            for i in range(19, len(prices)):
                std_[i] = prices[i-19 : i].std()
    
            for i in range(0, 19):
                upper_b[i] = None
                lower_b[i] = None
                middle_b[dates[i]] = None
                bb_output[dates[i]] = (middle_b[dates[i]], upper_b[i], lower_b[i])
            for i in range(19, len(prices)):
                upper_b[i] = middle_b[dates[i]] +(2 * std_[i])
                lower_b[i] = middle_b[dates[i]] -(2 * std_[i])
                upper_b[i] = float(round(upper_b[i]))
                lower_b[i] = float(round(lower_b[i]))
                bb_output[dates[i]] = (middle_b[dates[i]], upper_b[i], lower_b[i])
    
            return bb_output

    def rsi(self, period):
            
            dates = self.close.index
            prices = self.close.values
            
            rsi_output = {}
            
    
            for i in range(0, period -1):
                rsi_output[dates[i]] = None
            for i in range(period - 1, len(prices)):
                positive_day = []
                negative_day = []
                for _ in range(i - period, i):
                    
                    change = prices[_] - prices[_ - 1]
                    if change > 0:
                        positive_day.append(change)
                    else:
                        negative_day.append(change)
    
                average_gain = sum(positive_day) / period
    
                average_loss = abs(sum(negative_day)) / period
    
                rsi_output[dates[i]] = float(round(100-(100/(1+average_gain/average_loss)), 2))
    
            return rsi_output


    def band_width(self):
        bb_output = self.bollingerband()

        upper_band = [val[1] if val[1] is not None else np.nan for val in bb_output.values()]
        lower_band = [val[2] if val[2] is not None else np.nan for val in bb_output.values()]
        band_width = {}
        dates = self.close.index

        for i in range(0, len(bb_output)):
            band_width[dates[i]] = upper_band[i] - lower_band[i]

        rolling_band_width = pd.Series(band_width).rolling(window=20)
        band_width_sma_20 = rolling_band_width.mean()
        band_width_std_20 = rolling_band_width.std()

        return band_width, band_width_sma_20, band_width_std_20

    def volatility_marker(self):
        band_width_output = self.band_width()
        band_width, band_width_sma_20, band_width_std_20 = band_width_output
        volatility_marker = {}
        dates = self.close.index

        for i in range(0, len(band_width)):
            if band_width[dates[i]] > band_width_sma_20[dates[i]] + (2 * band_width_std_20[dates[i]]):
                volatility_marker[dates[i]] = False
            else:
                volatility_marker[dates[i]] = True
        return pd.Series(volatility_marker)

    def rsi_crossed_above(self, period=14 , level=30):
        rsi_output = pd.Series(self.rsi(period))
        dates = rsi_output.index
        rsi = rsi_output.values
        rsi_lower_crossover = {}

        rsi_lower_crossover[dates[0]] = False
        for i in range(1, len(dates)):
            if rsi[i-1] < level and rsi[i] >= level:
                rsi_lower_crossover[dates[i]] = True
            else:
                rsi_lower_crossover[dates[i]] = False

        rsi_lower_crossover = pd.Series(rsi_lower_crossover) 

        return rsi_lower_crossover


    def rsi_crossed_below(self, period=14 , level=70):
        rsi_output = pd.Series(self.rsi(period))
        dates = rsi_output.index
        rsi = rsi_output.values
        rsi_upper_crossover = {}

        rsi_upper_crossover[dates[0]] = False
        for i in range(1, len(dates)):
            if rsi[i-1] > level and rsi[i] <= level:
                rsi_upper_crossover[dates[i]] = True
            else:
                rsi_upper_crossover[dates[i]] = False

        rsi_upper_crossover = pd.Series(rsi_upper_crossover) 

        return rsi_upper_crossover

    def proximity_lower_band(self, pct):
        bb_output  = self.bollingerband()
        lower_band = [val[2] if val[2] is not None else np.nan for val in bb_output.values()]
        dates = self.close.index
        prices = self.close.values

        proximity_lower_band = {}


        for i in range(0, len(dates)):
            if (lower_band[i] - lower_band[i] * (pct/100)) < prices[i] < (lower_band[i] + lower_band[i] * (pct/100)):
                proximity_lower_band[dates[i]] = True
            else:
                proximity_lower_band[dates[i]] = False

        return pd.Series(proximity_lower_band)

    def proximity_upper_band(self, pct):
        bb_output  = self.bollingerband()
        upper_band = [val[1] if val[1] is not None else np.nan for val in bb_output.values()]
        dates = self.close.index
        prices = self.close.values

        proximity_upper_band = {}


        for i in range(0, len(dates)):
            if (upper_band[i] - upper_band[i] * (pct/100)) < prices[i] < (upper_band[i] + upper_band[i] * (pct/100)):
                proximity_upper_band[dates[i]] = True
            else:
                proximity_upper_band[dates[i]] = False

        return pd.Series(proximity_upper_band)

    def generate_signals(self, pct=2):
        proximity_upper = self.proximity_upper_band(pct)
        proximity_lower = self.proximity_lower_band(pct)
        rsi_above = self.rsi_crossed_above()
        rsi_below = self.rsi_crossed_below()
        vol_ok = self.volatility_marker()

        buy_signal = rsi_above & proximity_lower & vol_ok
        sell_signal = rsi_below & proximity_upper & vol_ok

        return buy_signal, sell_signal

    def visualize(self, show_rsi = True, show_bands = True, tick_interval=20):
        buy_signal, sell_signal = self.generate_signals()

        if show_rsi == True:
            n_panels = 2
        else: n_panels = 1
        fig, axes = plt.subplots(
            n_panels, 1,
            figsize=(14, 8 if show_rsi else 5),
            sharex=True,
            gridspec_kw={'height_ratios': [3, 1]} if show_rsi else None
        )
        price_ax = axes[0] if show_rsi else axes

        price_ax.plot(self.close.index, self.close.values, label="Close Price", color="black", linewidth=1)

        if show_bands:
            bb_output = self.bollingerband()
            dates = list(bb_output.keys())
            middle = [v[0] for v in bb_output.values()]
            upper = [v[1] for v in bb_output.values()]
            lower = [v[2] for v in bb_output.values()]

            price_ax.plot(dates, upper, label="Upper Band", color="blue", linestyle="--", linewidth=0.8)
            price_ax.plot(dates, middle, label="SMA 20", color="orange", linestyle="--", linewidth=0.8)
            price_ax.plot(dates, lower, label="Lower Band", color="blue", linestyle="--", linewidth=0.8)

        buy_dates = self.close[buy_signal]
        sell_dates = self.close[sell_signal]

        price_ax.scatter(buy_dates.index, buy_dates.values, marker="^", color="green", s=100, label="Buy", zorder=5)
        price_ax.scatter(sell_dates.index, sell_dates.values, marker="v", color="red", s=100, label="Sell", zorder=5)

        price_ax.set_ylabel("Price")
        price_ax.set_title("Price with Buy/Sell Signals")
        price_ax.legend(loc="upper left")

        if show_rsi:
            rsi_output = self.rsi(14)
            rsi_ax = axes[1]
            rsi_ax.plot(list(rsi_output.keys()), list(rsi_output.values()), label="RSI", color="purple", linewidth=1)
            rsi_ax.axhline(70, color="red", linestyle="--", linewidth=0.8)
            rsi_ax.axhline(30, color="green", linestyle="--", linewidth=0.8)
            rsi_ax.set_ylabel("RSI")
            rsi_ax.set_ylim(0, 100)
            rsi_ax.legend(loc="upper left")

        all_dates = list(self.close.index)
        tick_positions = all_dates[::tick_interval]
        bottom_ax = axes[-1] if show_rsi else price_ax
        bottom_ax.set_xticks(tick_positions)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


close_prices = {

    "Day 1": 100.00,
    "Day 2": 101.45,
    "Day 3": 99.80,
    "Day 4": 102.30,
    "Day 5": 101.10,
    "Day 6": 103.50,
    "Day 7": 104.20,
    "Day 8": 102.90,
    "Day 9": 105.15,
    "Day 10": 104.80,
    "Day 11": 106.30,
    "Day 12": 108.90,
    "Day 13": 107.40,
    "Day 14": 109.10,
    "Day 15": 111.25,
    "Day 16": 110.00,
    "Day 17": 108.50,
    "Day 18": 106.10,
    "Day 19": 107.30,
    "Day 20": 105.80,
    "Day 21": 104.20,
    "Day 22": 102.10,
    "Day 23": 103.40,
    "Day 24": 101.00,
    "Day 25": 99.50,
    "Day 26": 97.80,
    "Day 27": 98.90,
    "Day 28": 96.20,
    "Day 29": 94.50,
    "Day 30": 95.80,
    "Day 31": 96.40,
    "Day 32": 95.10,
    "Day 33": 97.30,
    "Day 34": 96.80,
    "Day 35": 98.20,
    "Day 36": 97.90,
    "Day 37": 99.10,
    "Day 38": 98.50,
    "Day 39": 100.40,
    "Day 40": 101.20,
    "Day 41": 100.80,
    "Day 42": 102.50,
    "Day 43": 101.90,
    "Day 44": 103.70,
    "Day 45": 104.30,
    "Day 46": 106.80,
    "Day 47": 105.20,
    "Day 48": 108.10,
    "Day 49": 110.50,
    "Day 50": 109.20,
    "Day 51": 112.40,
    "Day 52": 111.80,
    "Day 53": 114.30,
    "Day 54": 113.10,
    "Day 55": 115.60,
    "Day 56": 117.20,
    "Day 57": 116.00,
    "Day 58": 118.50,
    "Day 59": 117.90,
    "Day 60": 119.40,
    "Day 61": 116.20,
    "Day 62": 113.80,
    "Day 63": 114.50,
    "Day 64": 111.90,
    "Day 65": 109.30,
    "Day 66": 110.80,
    "Day 67": 107.40,
    "Day 68": 105.10,
    "Day 69": 106.30,
    "Day 70": 103.80,
    "Day 71": 102.20,
    "Day 72": 104.00,
    "Day 73": 101.50,
    "Day 74": 99.80,
    "Day 75": 101.10,
    "Day 76": 101.50,
    "Day 77": 100.90,
    "Day 78": 102.30,
    "Day 79": 101.80,
    "Day 80": 103.10,
    "Day 81": 102.60,
    "Day 82": 104.00,
    "Day 83": 103.40,
    "Day 84": 105.20,
    "Day 85": 104.70,
    "Day 86": 106.10,
    "Day 87": 105.80,
    "Day 88": 107.30,
    "Day 89": 106.90,
    "Day 90": 108.40,
    "Day 91": 111.20,
    "Day 92": 109.80,
    "Day 93": 113.50,
    "Day 94": 115.80,
    "Day 95": 114.10,
    "Day 96": 117.60,
    "Day 97": 116.20,
    "Day 98": 119.80,
    "Day 99": 121.40,
    "Day 100": 120.10,
    "Day 101": 123.50,
    "Day 102": 122.00,
    "Day 103": 125.80,
    "Day 104": 124.30,
    "Day 105": 127.90,
    "Day 106": 125.10,
    "Day 107": 122.40,
    "Day 108": 123.80,
    "Day 109": 120.20,
    "Day 110": 118.50,
    "Day 111": 119.90,
    "Day 112": 116.30,
    "Day 113": 114.80,
    "Day 114": 116.10,
    "Day 115": 113.40,
    "Day 116": 111.90,
    "Day 117": 113.20,
    "Day 118": 110.60,
    "Day 119": 108.90,
    "Day 120": 110.30,
    "Day 121": 110.80,
    "Day 122": 111.50,
    "Day 123": 110.90,
    "Day 124": 112.30,
    "Day 125": 111.80,
    "Day 126": 113.40,
    "Day 127": 112.90,
    "Day 128": 114.20,
    "Day 129": 113.70,
    "Day 130": 115.10,
    "Day 131": 114.60,
    "Day 132": 116.00,
    "Day 133": 115.50,
    "Day 134": 117.20,
    "Day 135": 116.80,
    "Day 136": 119.50,
    "Day 137": 118.10,
    "Day 138": 121.80,
    "Day 139": 120.40,
    "Day 140": 123.90,
    "Day 141": 122.30,
    "Day 142": 125.70,
    "Day 143": 124.20,
    "Day 144": 127.80,
    "Day 145": 126.30,
    "Day 146": 129.50,
    "Day 147": 128.10,
    "Day 148": 131.40,
    "Day 149": 129.80,
    "Day 150": 132.60


}

# Test #
test = Signal(close_prices)
result = test.generate_signals(2)
test.visualize()

