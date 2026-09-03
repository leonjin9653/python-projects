import pandas as pd
import numpy as np

class Signal():
    def __init__(self, close_prices):
        self.close = pd.Series(close_prices)

    def bollingerband(self):
            bb_output = {}
    
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


    def band_width(self, bb_output):
        def series(index):
            extracted_values = []
            for value in bb_output.values():
                if value is not None:
                    extracted_values.append(value[index])
                else:
                    extracted_values.append(np.nan)
            return extracted_values

        upper_band = series(1)
        lower_band = series(2)
        band_width = {}
        

        for i in range(0, len(bb_output)):
            band_width[i] = upper_band[i] - lower_band[i]

        rolling_band_width = pd.Series(band_width).rolling(window=20)
        band_width_sma_20 = rolling_band_width.mean()
        band_width_std_20 = rolling_band_width.std()

        return band_width, band_width_sma_20, band_width_std_20

    def volatility_marker(band_width, band_width_sma_20, band_width_std_20):
        return band_width <= band_width_sma_20 + (2 * band_width_std_20)

    # Hi leon. So basically the buy signal and sell signal require 2 indiactors.
    # Firstly, to buy, the rsi must have the conditions that rsi[i] >= 30 and rsi[i-1] < 30
    # This determines that it is crossing the 30 lower limit with upwards momentum.
    # Secondly, the price must be within 2% of the lower bollinger band. 
    # This indicates that the price is below 2 standard deviations of its 20 period average
    # This would signal an increase and return to the average, in tandem with the rsi signal.
    # Both conditions along with the overarching volatility filter must be in compliance
    # in order for a buy signal. 
    # The reverse is in order for the sell signal. 

    def rsi_crossed_above(rsi_output, level=30):
        


    def rsi_crossed_below(rsi_output, level=70):


    
        



        
    



close_prices = {}