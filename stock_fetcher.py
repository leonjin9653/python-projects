"""
Real Stock Data Fetcher
Tier 2 Python Project - pulls live market data via yfinance.
"""

import yfinance as yf
from datetime import datetime


class StockData:
    """Wraps a yfinance Ticker to give clean access to real market data."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self._info = None  # lazy-loaded cache

    @property
    def info(self):
        """Lazy-load and cache the .info dict (it's a slow network call)."""
        if self._info is None:
            self._info = self.ticker.info
        return self._info

    def current_price(self) -> float:
        return self.info.get("currentPrice") or self.info.get("regularMarketPrice")

    def name(self) -> str:
        return self.info.get("shortName", self.symbol)

    def market_cap(self) -> float:
        return self.info.get("marketCap")

    def pe_ratio(self) -> float:
        return self.info.get("trailingPE")

    def day_range(self) -> tuple:
        return self.info.get("dayLow"), self.info.get("dayHigh")

    def fifty_two_week_range(self) -> tuple:
        return self.info.get("fiftyTwoWeekLow"), self.info.get("fiftyTwoWeekHigh")

    def history(self, period: str = "1mo"):
        """Returns a pandas DataFrame of historical OHLCV data.
        period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        return self.ticker.history(period=period)

    def summary(self) -> str:
        low, high = self.day_range()
        yr_low, yr_high = self.fifty_two_week_range()
        lines = [
            f"{self.name()} ({self.symbol})",
            f"  Price:        ${self.current_price():.2f}" if self.current_price() else "  Price:        N/A",
            f"  Day Range:    ${low} - ${high}" if low and high else "  Day Range:    N/A",
            f"  52wk Range:   ${yr_low} - ${yr_high}" if yr_low and yr_high else "  52wk Range:   N/A",
            f"  Market Cap:   ${self.market_cap():,}" if self.market_cap() else "  Market Cap:   N/A",
            f"  P/E Ratio:    {self.pe_ratio():.2f}" if self.pe_ratio() else "  P/E Ratio:    N/A",
        ]
        return "\n".join(lines)


def main():
    print("=== Stock Data Fetcher ===")
    print("Enter a ticker symbol (or 'quit' to exit)\n")

    while True:
        symbol = input("Ticker: ").strip()
        if symbol.lower() in ("quit", "exit", "q"):
            break
        if not symbol:
            continue

        try:
            stock = StockData(symbol)
            print()
            print(stock.summary())
            print()
        except Exception as e:
            print(f"Error fetching {symbol}: {e}\n")


if __name__ == "__main__":
    main()
