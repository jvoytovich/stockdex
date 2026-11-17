Data Sources
============

Each data source returns pandas DataFrames. Every method name starts with
its source, e.g. ``yahoo_api_income_statement`` or ``finviz_revenue_by_segment``.

.. list-table::
   :header-rows: 1
   :widths: 18 18 64

   * - Source
     - Prefix
     - Best for
   * - Yahoo Finance
     - ``yahoo_api_``
     - Prices, statements, valuation, profile, analyst estimates, ownership,
       SEC filings, ETF and fund data, options and search
   * - Yahoo Finance (website)
     - ``yahoo_web_``
     - The original website scraper (restored on the ``super`` branch of
       jvoytovich/stockdex): statements, summary, valuation measures,
       analyst estimates, holders, options and profile in the website's layout
   * - Digrin
     - ``digrin_``
     - Full dividend history, payout ratio, dividend growth rate and
       long-term fundamentals
   * - Macrotrends
     - ``macrotrends_``
     - Up to 15 years of statements, margins, ratios and revenue
   * - Finviz
     - ``finviz_``
     - Insider trades, revenue by segment, region and product, earnings
       history and revisions
   * - justETF
     - ``justetf_``
     - European ETFs by ISIN

.. note::
   Upstream stockdex deprecated the ``yahoo_web_*`` methods in 1.5.0 (they
   only forwarded to ``yahoo_api_*``) and plans to remove them in 2.0. This
   ``super`` branch keeps 1.6.0 and puts the real website scraper back behind
   those names; see the :doc:`changelog`.

.. toctree::
   :maxdepth: 1

   readme_files/raw_dataframes/yahoo_api_doc
   readme_files/raw_dataframes/yahoo_web_doc
   readme_files/raw_dataframes/finviz_doc
   readme_files/raw_dataframes/digrin_doc
   readme_files/raw_dataframes/macrotrends_doc
   readme_files/raw_dataframes/justetf_doc