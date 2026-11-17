"""Offline tests for yahoo_api_company_name, the Macrotrends slug and statement dates.

Kept from upstream's test_yahoo_web_deprecated.py (1.5.0+); the deprecated
yahoo_web_* aliases they sat next to are replaced by the real scraper on this
branch, so only the tests that don't depend on the aliases are kept here.
"""

import warnings
from datetime import datetime, timedelta

import pandas as pd
import pytest

from stockdex import Ticker


@pytest.fixture
def ticker(monkeypatch):
    """A Ticker whose yahoo_api_market_price returns canned data, no network."""
    ticker = Ticker("AAPL")
    monkeypatch.setattr(
        ticker,
        "yahoo_api_market_price",
        lambda: pd.DataFrame(
            {"AAPL": ["Apple Inc.", "Apple"]}, index=["longName", "shortName"]
        ),
    )
    return ticker


def test_company_name(ticker):
    assert ticker.yahoo_api_company_name() == "Apple Inc."


@pytest.mark.parametrize(
    "index, values, expected",
    [
        (["shortName"], ["Apple"], "Apple"),
        (["longName", "shortName"], [None, "Apple"], "Apple"),
        (["regularMarketPrice"], [1.0], "AAPL"),
    ],
)
def test_company_name_fallbacks(monkeypatch, index, values, expected):
    ticker = Ticker("AAPL")
    monkeypatch.setattr(
        ticker,
        "yahoo_api_market_price",
        lambda: pd.DataFrame({"AAPL": values}, index=index),
    )
    assert ticker.yahoo_api_company_name() == expected


def test_macrotrends_full_name_uses_api(monkeypatch):
    ticker = Ticker("BRK-B")
    monkeypatch.setattr(
        ticker, "yahoo_api_company_name", lambda: "Berkshire Hathaway Inc."
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert ticker.full_name == "berkshire-hathaway-inc"


def test_statement_dates_resolved_per_call(monkeypatch):
    ticker = Ticker("AAPL")
    urls = []

    class Response:
        def json(self):
            return {"timeseries": {"result": []}}

    monkeypatch.setattr(
        ticker, "get_response", lambda url: urls.append(url) or Response()
    )
    before = datetime.today()
    ticker.yahoo_api_income_statement()
    params = dict(p.split("=") for p in urls[-1].split("?", 1)[1].split("&"))
    # build_url reads naive datetimes as UTC, so read them back the same way
    period2 = pd.Timestamp(int(params["period2"]), unit="s").to_pydatetime()
    period1 = pd.Timestamp(int(params["period1"]), unit="s").to_pydatetime()
    assert abs(period2 - before) < timedelta(minutes=1)
    assert 365 * 5 - 2 <= (period2 - period1).days <= 365 * 5 + 2


def test_yahoo_web_scraper_is_mixed_in():
    """On this branch Ticker uses the real website scraper, not aliases."""
    from stockdex.yahoo_web_interface import YahooWeb

    assert issubclass(Ticker, YahooWeb)
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert callable(Ticker("AAPL").yahoo_web_financials_table)
