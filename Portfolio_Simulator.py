class Stock: 
    def __init__(self, ticker, shares_owned, avg_purchase_price):
        self.ticker = ticker
        self.shares_owned = shares_owned
        self.avg_purchase_price = avg_purchase_price


apple_stock = Stock("AAPL", 10, 150.00)
SP500_stock = Stock("INDEXSP", 100, 7500.00)

print(apple_stock.ticker)
print(SP500_stock.ticker)
