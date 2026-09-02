import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Technical_Indicator():
    def __init__(self, close_prices):
        self.close = pd.Series(close_prices)

    def graph(self, result, kind, overlay="no"):
        dates = list(self.close.index)
        prices = self.close.values
        kind = kind.lower().strip()
        overlay = overlay.lower().strip()

        def series(index):
            return [v[index] if v is not None else np.nan for v in result.values()]

        def scalar_series():
            return [v if v is not None else np.nan for v in result.values()]

        fig, ax = plt.subplots(figsize=(10, 5))

        if kind in ("sma", "ema"):
            values = scalar_series()
            if overlay == "yes":
                ax.plot(dates, prices, label="Price", color="black", alpha=0.6)
                ax.plot(dates, values, label=kind.upper())
                ax.set_title(f"Price with {kind.upper()}")
            else:
                plt.close(fig)
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
                ax1.plot(dates, prices, label="Price")
                ax1.set_title("Price")
                ax1.legend()
                ax2.plot(dates, values, label=kind.upper(), color="orange")
                ax2.set_title(kind.upper())
                ax2.legend()
                ax2.xaxis.set_major_locator(MaxNLocator(nbins=10))
                plt.tight_layout()
                plt.show()
                return

        elif kind == "rsi":
            ax.plot(dates, scalar_series(), label="RSI", color="purple")
            ax.axhline(70, color="red", linestyle="--", linewidth=1)
            ax.axhline(30, color="green", linestyle="--", linewidth=1)
            ax.set_ylim(0, 100)
            ax.set_title("RSI")

        elif kind == "macd":
            ax.plot(dates, series(0), label="MACD", color="blue")
            ax.plot(dates, series(1), label="Signal", color="orange")
            ax.bar(dates, series(2), label="Histogram", color="gray", alpha=0.5)
            ax.set_title("MACD")

        elif kind == "bollinger":
            ax.plot(dates, prices, label="Price", color="black", alpha=0.6)
            ax.plot(dates, series(0), label="Middle Band", color="blue")
            ax.plot(dates, series(1), label="Upper Band", color="red", linestyle="--")
            ax.plot(dates, series(2), label="Lower Band", color="green", linestyle="--")
            ax.set_title("Bollinger Bands")

        else:
            print(f"Unknown indicator kind: '{kind}'")
            plt.close(fig)
            return

        ax.set_xlabel("Date")
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.tight_layout()
        plt.show()


    def sma(self, period):
        output = {}
        dates = self.close.index
        prices = self.close.values

        if period > len(prices):
            print(f"Period exceeds limit for any calculation. Error.")
            return

        for i in range(0, period-1):
            output[dates[i]] = None
        for i in range(period - 1, len(prices)):
            window_sum = sum(prices[i-period + 1 : i+1])
            
            output[dates[i]] = float(round(window_sum/period, 2))

        return output 

    def ema(self, period):
        output = {}
        dates = self.close.index
        prices = self.close.values

        smoothing_constant = 2/ (period + 1)

        for i in range(0, period -1):
            output[dates[i]] = None

        seed = sum(prices[0 : period])/ period
        output[dates[period -1]] = float(round(seed, 2))

        for i in range(period, len(prices)):
            part1 = prices[i] * smoothing_constant
            part2 = output[dates[i-1]] * (1 - smoothing_constant)
            output[dates[i]] = float(round(part1 + part2, 2)) 

        return output

    def rsi(self, period):
        
        dates = self.close.index
        prices = self.close.values
        
        output = {}
        

        for i in range(0, period -1):
            output[dates[i]] = None
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

            output[dates[i]] = float(round(100-(100/(1+average_gain/average_loss)), 2))

        return output

    def macd(self):
        output = {}
        macd_line = {}
        signal_line = {}

        dates = self.close.index

        fast_ema = self.ema(12)
        slow_ema = self.ema(26)

        for date in dates:
            f = fast_ema[date]
            s = slow_ema[date]
            if f is not None and s is not None:
                macd_line[date] = float(round(f-s, 2)) 
            else:
                macd_line[date] = None

        valid_dates = [d for d in dates if macd_line[d] is not None]

        if len(valid_dates) < 9:
            for d in dates:
                output[d] = None
            return output
        for d in dates:
            if d not in valid_dates:
                output[d] = None
        for i in range(8):
            signal_line[valid_dates[i]] = None
            output[valid_dates[i]] = None

        seed = sum(macd_line[d] for d in valid_dates[:9]) / 9
        seed_date = valid_dates[8]
        signal_line[seed_date] = float(round(seed, 2))
        output[seed_date] = (macd_line[seed_date], signal_line[seed_date],
                            float(round(macd_line[seed_date] - signal_line[seed_date], 2)))

        smoothing_constant = 2 / (10)
        for i in range(9, len(valid_dates)):
            d, prev_d = valid_dates[i], valid_dates[i - 1]
            sig = macd_line[d] * smoothing_constant + signal_line[prev_d] * (1 - smoothing_constant)
            signal_line[d] = float(round(sig, 2))
            hist = float(round(macd_line[d] - signal_line[d], 2))
            output[d] = (macd_line[d], signal_line[d], hist)

        return output

    def bollingerband(self):
        output = {}

        dates = self.close.index
        prices = self.close.values

        upper_b = {}
        lower_b = {}
        
        middle_b = self.sma(20)
        
        std_ = {}

        for i in range(0, 19):
            std_[i] = None
        for i in range(19, len(prices)):
            std_[i] = prices[i-19 : i].std()

        for i in range(0, 19):
            upper_b[i] = None
            lower_b[i] = None
            middle_b[dates[i]] = None
            output[dates[i]] = (middle_b[dates[i]], upper_b[i], lower_b[i])
        for i in range(19, len(prices)):
            upper_b[i] = middle_b[dates[i]] +(2 * std_[i])
            lower_b[i] = middle_b[dates[i]] -(2 * std_[i])
            upper_b[i] = float(round(upper_b[i]))
            lower_b[i] = float(round(lower_b[i]))
            output[dates[i]] = (middle_b[dates[i]], upper_b[i], lower_b[i])

        return output
            
            



            

### price library 
close_prices ={

    "Day 1": 5,
    "Day 2": 7,
    "Day 3": 9,
    "Day 4": 5,
    "Day 5": 2,
    "Day 6": 4,
    "Day 7": 1,
    "Day 8": 6,
    "Day 9": 8,
    "Day 10": 9,
    "Day 11": 10,
    "Day 12": 12,
    "Day 13": 15,
    "Day 14": 16,
    "Day 15": 12,
    "Day 16": 15,
    "Day 17": 15,
    "Day 18": 16,
    "Day 19": 12,
    "Day 20": 17,
    "Day 21": 20,
    "Day 22": 24,
    "Day 23": 25,
    "Day 24": 28,
    "Day 25": 30,
    "Day 26": 28,
    "Day 27": 26,
    "Day 28": 29,
    "Day 29": 31,
    "Day 30": 27,
    "Day 31": 24,
    "Day 32": 26,
    "Day 33": 23,
    "Day 34": 25,
    "Day 35": 28,
    "Day 36": 32,
    "Day 37": 30,
    "Day 38": 33,
    "Day 39": 35,
    "Day 40": 32,
    "Day 41": 29,
    "Day 42": 31,
    "Day 43": 27,
    "Day 44": 25,
    "Day 45": 28,
    "Day 46": 30,
    "Day 47": 34,
    "Day 48": 32,
    "Day 49": 36,
    "Day 50": 38,
    "Day 51": 35,
    "Day 52": 31,
    "Day 53": 33,
    "Day 54": 29,
    "Day 55": 32,
    "Day 56": 34,
    "Day 57": 37,
    "Day 58": 35,
    "Day 59": 39,
    "Day 60": 42,
    "Day 61": 39,
    "Day 62": 36,
    "Day 63": 38,
    "Day 64": 34,
    "Day 65": 37,
    "Day 66": 40,
    "Day 67": 38,
    "Day 68": 41,
    "Day 69": 44,
    "Day 70": 42,
    "Day 71": 38,
    "Day 72": 40,
    "Day 73": 36,
    "Day 74": 39,
    "Day 75": 43,
    "Day 76": 41,
    "Day 77": 45,
    "Day 78": 42,
    "Day 79": 39,
    "Day 80": 41,
    "Day 81": 37,
    "Day 82": 40,
    "Day 83": 44,
    "Day 84": 46,
    "Day 85": 43,
    "Day 86": 47,
    "Day 87": 45,
    "Day 88": 41,
    "Day 89": 43,
    "Day 90": 38,
    "Day 91": 41,
    "Day 92": 45,
    "Day 93": 48,
    "Day 94": 46,
    "Day 95": 50,
    "Day 96": 47,
    "Day 97": 43,
    "Day 98": 45,
    "Day 99": 40,
    "Day 100": 42,
    "Day 101": 46,
    "Day 102": 49,
    "Day 103": 47,
    "Day 104": 51,
    "Day 105": 48,
    "Day 106": 44,
    "Day 107": 46,
    "Day 108": 41,
    "Day 109": 43,
    "Day 110": 47,
    "Day 111": 50,
    "Day 112": 48,
    "Day 113": 52,
    "Day 114": 49,
    "Day 115": 45,
    "Day 116": 47,
    "Day 117": 42,
    "Day 118": 44,
    "Day 119": 48,
    "Day 120": 51,
    "Day 121": 49,
    "Day 122": 53,
    "Day 123": 50,
    "Day 124": 46,
    "Day 125": 48,
    "Day 126": 43,
    "Day 127": 45,
    "Day 128": 49,
    "Day 129": 52,
    "Day 130": 50,
    "Day 131": 54,
    "Day 132": 51,
    "Day 133": 47,
    "Day 134": 49,
    "Day 135": 44,
    "Day 136": 46,
    "Day 137": 50,
    "Day 138": 53,
    "Day 139": 51,
    "Day 140": 55,
    "Day 141": 52,
    "Day 142": 48,
    "Day 143": 50,
    "Day 144": 45,
    "Day 145": 47,
    "Day 146": 51,
    "Day 147": 54,
    "Day 148": 52,
    "Day 149": 56,
    "Day 150": 53,

}

### testing ###
test = Technical_Indicator(close_prices)
result = test.bollingerband()
print(result)
test.graph(result, kind="bollinger")
