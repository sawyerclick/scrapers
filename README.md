# GitHub Actions scrapers

## School covid

- [WVU COVID-19 testing & cases](https://www.wvu.edu/return-to-campus/daily-test-results/morgantown/all)
<code>wvu-covid/scrape.py</code> runs every Wednesday at 2:04 p.m. and captures the latest testing, isolating, self-reporting and quarantine data from the school. All four tables are scraped and parsed iteratively via BeautifulSoup and a GitHub Action.

<hr>

## Headlines
Scraping headlines from the home pages of news orgs

- SFChronicle.com
