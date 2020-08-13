import csv
import re

import requests
from bs4 import BeautifulSoup


# Get html from url.
def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


# Clear price.
def refined(s):
    # $11,254.41
    return s.replace('$', '').replace('.', '').replace(',', '')


# Write in csv file.
def write_csv(data):
    with open('cmc.csv', 'a') as f:
        order = ['name', 'url', 'price']

        writer = csv.DictWriter(f, order)

        writer.writerow(data)


        writer.writerow((
            data['name'],
            data['url'],
            data['price'],
        ))


# Parse data from html to write in csv.
def parse_data(html):
    soup = BeautifulSoup(html, 'lxml')

    container = soup.find('body').find('div', class_='cmc-main-section__content')
    tables = container.find_all('table')
    trs = tables[2].find('tbody').find_all('tr', class_='cmc-table-row')

    for tr in trs:
        tds = tr.find_all('td')
        try:
            name = tds[1].find('a').text
        except:
            name = ''

        try:
            url = 'https://coinmarketcap.com' + tds[1].find('a').get('href')
        except:
            url = ''

        try:
            # price = tds[3].find('a').get('data-usd').strip()
            price = refined(tds[3].text)
        except:
            price = ''

        data = {
            'name': name,
            'url': url,
            'price': price,
        }

        write_csv(data)


def main():
    url = 'https://coinmarketcap.com/'

    while True:
        # Get html
        html = get_html(url)

        # Write data to csv file
        parse_data(html)

        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            pattern = 'Next'
            regex = re.compile(pattern)

            # Get href from pagination
            pagination = soup.find('div', class_='cmc-table-listing__pagination')
            href = pagination.find('a', text=regex).get('href')

            # Change url
            url = 'https://coinmarketcap.com' + href

        except:
            print('Not found')
            break


if __name__ == '__main__':
    main()
