#!/usr/bin/env python3

from attrdict import AttrDict
import mechanicalsoup
import json


def main():
    args = get_args()
    browser = mechanicalsoup.Browser(
        soup_config={'features': 'lxml'},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    )
    results = []
    if args.verbose:
        print("Starting to crawl. Options:\n{}\n\n".format(args))

    for page_num in range(args.page_start, args.page_end + 1):
        url = args.url % ('seite:' + str(page_num))
        if args.verbose:
            print(
                "\tCrawling page: {:2}/{:2} ({})\n\n".format(page_num, args.page_end, url))
        page = browser.get(url)
        domain = '/'.join(url.split('/')[0:3])     # Dirty
        results += get_results(page, domain)
        if not page.soup.select('.pagination-next'):
            if args.verbose:
                print(
                    "Stop crawling because last seen page does not contain a next-page button, so all results are already fetched")
            break

    print(json.dumps(results, sort_keys=True))


def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Crawl ebay kleinanzeigen', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url', default='https://www.ebay-kleinanzeigen.de/s-saarbruecken/%s/peugeot/k0l382',
                        help='The start url. Must have a [percent-sign]s portion in the url to insert the "options" like the page num, price etc.')
    parser.add_argument('--page-start', default=1, type=int,
                        help='The page number to start at')
    parser.add_argument('--page-end', default=10, type=int,
                        help='The page number to end at (may end before if less results found)')
    parser.add_argument('--options', default='',
                        help='Options for kleinanzeigen. Get from the site. Example: "--options preis:0:20"')
    parser.add_argument('--verbose', default=False, action='store_true')
    args = parser.parse_args()
    args.url = args.url % (args.options + '/%s')
    return args


def get_results(page, domain):
    results = []
    for el in page.soup.select('article.aditem'):
        out = AttrDict()
        out.link = domain + el.select('a[href^="/s-anzeige"]')[0].attrs['href']
        out.title = el.select('.text-module-begin a')[0].text.strip()
        out.desc = el.select('.aditem-main p')[0].text.strip()
        out.price = el.select('.aditem-main--middle--price')[0].text.strip()
        out.location = el.select('.aditem-main--top--left')[0].text.strip()
        img = el.select('[data-imgsrc]')
        out.img = img[0].attrs['data-imgsrc'] if len(img) else None
        results.append(out)
    return results


if __name__ == '__main__':
    main()
