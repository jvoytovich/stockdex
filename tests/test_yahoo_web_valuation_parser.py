"""Offline tests for the Yahoo key-statistics valuation measures parser."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from stockdex import Ticker
from stockdex.exceptions import NoDataError

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "yahoo"


def fixture_ticker(monkeypatch, html):
    ticker = Ticker("AAPL")
    monkeypatch.setattr(
        ticker, "get_response", lambda url: SimpleNamespace(content=html.encode())
    )
    return ticker


def test_valid_page(monkeypatch):
    html = (FIXTURES / "key_statistics_valid.html").read_text()
    frame = fixture_ticker(monkeypatch, html).yahoo_web_valuation_measures
    assert list(frame.columns) == ["Current", "6/30/2026", "3/31/2026"]
    assert frame.loc["Market Cap", "Current"] == "5.15T"
    assert frame.shape == (2, 3)


def test_h2_layout_page(monkeypatch):
    html = (FIXTURES / "key_statistics_h2_layout.html").read_text()
    frame = fixture_ticker(monkeypatch, html).yahoo_web_valuation_measures
    assert list(frame.columns) == ["Current", "9/30/2026", "6/30/2026"]
    assert frame.loc["Market Cap", "Current"] == "5.13T"
    assert frame.shape == (2, 3)


@pytest.mark.parametrize(
    "html",
    [
        "<html><body>Consent required</body></html>",
        "<div><h2>Valuation Measures</h2></div>",
        "<section><header><h3>Valuation Measures</h3></header></section>",
        "<section><header><h3>Valuation Measures</h3></header>"
        "<table><tr><td>x</td></tr></table></section>",
    ],
)
def test_missing_section_raises_no_data(monkeypatch, html):
    with pytest.raises(NoDataError):
        _ = fixture_ticker(monkeypatch, html).yahoo_web_valuation_measures
