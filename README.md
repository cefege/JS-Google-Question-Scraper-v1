# GoogleScrapper

This is a Python package for scraping Google search results for a specific query. It uses the `playwright` library to interact with a Chromium browser and simulate user clicks on the search page. The package is designed to work with Python 3.7 and higher.

## Installation

You can install the package via pip:

```bash
pip install git+https://github.com/cefege/Question-Scraper.git
```

## Usage

To use the package, you need to provide a query to search for, and the number of questions to scrape (optional). Here's an example:

```python
from google_scrapper import scrapper_g

# scrape 5 questions for the query "how to learn python"
results = scrapper_g("how to learn python", num_questions_to_scraper=5)
print(results)
```

The `scrapper_g` function takes four arguments:
- `query`: the query to search for.
- `num_questions_to_scraper`: the number of questions to scrape. If not provided, it will scrape all questions found on the page.
- `headless_mode`: Whether to run the browser in headless mode or not. If not provided, it will run in headless mode by default.
- `proxy`: The proxy to use. If not provided, it will not use a proxy.

The `scrapper_g` function returns a string containing the HTML content of the scraped page.
