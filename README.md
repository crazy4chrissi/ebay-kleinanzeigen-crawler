# eBay Kleinanzeigen Crawler

Crawls ebay Kleinanzeigen end extract data as JSON.

## Instructions

```bash
pip3 install -r requirements.txt
./crawl.py > results.json
```

## Usage

```
usage: crawl.py [-h] [--url URL] [--page-start PAGE_START]
                [--page-end PAGE_END] [--json-out JSON_OUT]
                [--options OPTIONS] [--verbose] [--details]

Crawl ebay kleinanzeigen

optional arguments:
  -h, --help            Show this help message and exit
  --url URL             The start url. Must have a [percent-sign]s portion in
                        the url to insert the "options" like the page num,
                        price etc. (default: https://www.ebay-
                        kleinanzeigen.de/s-64283/%s/l4896)
  --page-start PAGE_START
                        The page number to start at (default: 1)
  --page-end PAGE_END   The page number to end at (may end before if less
                        results found, default: 10)
  --options OPTIONS     Options for kleinanzeigen. Get from the site (example:
                        preis:0:20/, default:)
  --verbose             Print verbose output before result JSON
  --details             Crawl the details page of each ad in order to obtain
                        more details. Requires a lot more requests.
```
