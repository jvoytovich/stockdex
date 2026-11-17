"""Offline test for yahoo_web_top_mutual_fund_holders (no network)."""

import pytest

from stockdex import Ticker
from stockdex.exceptions import NoDataError


def _table(rows):
    header = "<tr><th>Holder</th><th>Shares</th><th>Date Reported</th><th>% Out</th><th>Value</th></tr>"
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f"<table>{header}{body}</table>"


HOLDERS_PAGE = f"""
<div>
  <section data-testid="holders-major-holders-table">
    <table><tr><td>1.69%</td><td>% of Shares Held by All Insider</td></tr></table>
  </section>
  <section data-testid="holders-top-institutional-holders">
    <h3>Top Institutional Holders</h3>
    {_table([["Blackrock Inc.", "1.16B", "Sep 30, 2026", "7.96%", "405,694,451,651"]])}
  </section>
  <section data-testid="holders-top-mutual-fund-holders">
    <h3>Top Mutual Fund Holders</h3>
    {_table([
        ["VANGUARD INDEX FUNDS", "466.27M", "Jun 30, 2026", "3.21%", "163,484,371,914"],
        ["Invesco QQQ Trust, Series 1", "110.42M", "Sep 30, 2026", "0.76%", "38,715,606,419"],
    ])}
  </section>
</div>
"""


class _Response:
    def __init__(self, html):
        self.content = html.encode()


def test_mutual_fund_holders_reads_only_its_table(monkeypatch):
    ticker = Ticker("AAPL")
    monkeypatch.setattr(ticker, "get_response", lambda url: _Response(HOLDERS_PAGE))

    frame = ticker.yahoo_web_top_mutual_fund_holders

    assert list(frame.columns) == [
        "holder",
        "shares",
        "date_reported",
        "percentage",
        "value",
    ]
    assert frame["holder"].tolist() == [
        "VANGUARD INDEX FUNDS",
        "Invesco QQQ Trust, Series 1",
    ]
    assert not frame.isna().any().any()


def test_mutual_fund_holders_missing_section(monkeypatch):
    ticker = Ticker("AAPL")
    monkeypatch.setattr(ticker, "get_response", lambda url: _Response("<html></html>"))
    with pytest.raises(NoDataError):
        _ = ticker.yahoo_web_top_mutual_fund_holders
