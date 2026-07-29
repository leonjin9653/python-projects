class Stock: 
    def __init__(self, ticker, shares_owned, avg_purchase_price):
        self.ticker = ticker
        self.shares_owned = shares_owned
        self.avg_purchase_price = avg_purchase_price
    def current_value(self, current_price):
        return self.shares_owned * current_price
    def profit_loss(self, current_price):
        return (current_price - self.avg_purchase_price) * self.shares_owned
        
class Portfolio:
    def __init__(self, starting_cash):
        self.cash_balance = starting_cash
        self.holdings = {}
    def calculate_new_avg_price(self, old_shares, old_avg_price, new_shares, new_price):
        total_cost = (old_shares * old_avg_price) + (new_shares * new_price)
        total_shares = old_shares + new_shares
        new_avg_price = total_cost/ total_shares
        return new_avg_price, total_shares
    def buy(self, ticker, shares, price):
        total_cost = shares * price
        if total_cost > self.cash_balance:
            print("Purchase Denied")
            return 
        else:
            self.cash_balance = self.cash_balance - total_cost
        if ticker in self.holdings:
            existing_stock = self.holdings[ticker]
            new_avg_price = self.calculate_new_avg_price(
                existing_stock.shares_owned, 
                existing_stock.avg_purchase_price, shares, price
                )
            avg_price, total_shares = new_avg_price #unpacks the tuple 
            # as calculate_new_avg_price returns a tuple
            existing_stock.avg_purchase_price = avg_price
            existing_stock.shares_owned = total_shares
            return
        else:
            self.holdings[ticker] = Stock(ticker, shares, price)
    def sell(self, ticker, shares, price):
        if ticker in self.holdings:
            existing_stock = self.holdings[ticker]
            if shares>existing_stock.shares_owned:
                print("Sale Denied")
                return
            elif shares == existing_stock.shares_owned:
                total_cost = shares* price
                self.cash_balance = self.cash_balance + total_cost
                del self.holdings[ticker]
                return     
            total_cost = shares * price
            self.cash_balance = self.cash_balance + total_cost
            existing_stock.shares_owned = existing_stock.shares_owned - shares

    def display_holdings(self):
        print(f"Cash Balance: ${self.cash_balance}")
        for ticker, stock in self.holdings.items():
            print(f"Ticker: {ticker}, Shares Owned: {stock.shares_owned}, Average Purchase Price: ${stock.avg_purchase_price}")
    def total_value(self, current_prices):
        total_value = 0 
        for ticker, stock in self.holdings.items():
            if ticker in current_prices:
                current_price = current_prices[ticker]
                total_value = total_value + stock.current_value(current_price)
            else:
                print(f"Current price for {ticker} not found.")
        return total_value
    def total_portfolio_value(self, current_prices):
        total_portfolio_value = 0 
        total_portfolio_value = self.total_value(current_prices) + self.cash_balance
        return total_portfolio_value



'''
apple_stock = Stock("AAPL", 10, 150.00)
value_apple = apple_stock.current_value(170.00)
profit_loss_apple = apple_stock.profit_loss(170.00)

SP500_stock = Stock("SP500", 5, 7500.00)
value_SP500 = SP500_stock.current_value(7450.00)
profit_loss_SP500 = SP500_stock.profit_loss(7450.00)


print(f"Stock: {apple_stock.ticker}")
print(f"Shares owned: {apple_stock.shares_owned}")
print(f"Valuation: {value_apple}")
print(f"Profit/Loss: {profit_loss_apple}")
print(f"Stock: {SP500_stock.ticker}")
print(f"Shares owned: {SP500_stock.shares_owned}")
print(f"Valuation: {value_SP500}")
print(f"Profit/Loss: {profit_loss_SP500}")
'''
### test script

current_prices = {
    "AAPL": 170.00,
    "SP500": 7600.00
}

my_portfolio = Portfolio(100000.00)
my_portfolio.buy("AAPL", 10, 170)
buy_apple = my_portfolio.buy("AAPL", 25, 170)
buy_SP500 = my_portfolio.buy("SP500",10, 7600)
sell_SP500 = my_portfolio.sell("SP500", 2, 7300)

my_portfolio.display_holdings()
print(f"Total Stock Value: ${my_portfolio.total_value(current_prices)}")
print(f"Total Portfolio Value: ${my_portfolio.total_portfolio_value(current_prices)}")

