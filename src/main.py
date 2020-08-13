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
def write_csv(file_name, data, order):
    with open(file_name, 'a') as f:
        writer = csv.DictWriter(f, order)

        writer.writerow(data)


# Read data from csv file.
def read_csv(file_name, field_names):
    with open(file_name) as file:
        reader = csv.DictReader(file, field_names)

        for row in reader:
            print(row)


# Parse data from html to write in csv.
def parse_and_send_to_write_data(file_name, html, labels):
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

        # Todo: from labels
        data = {
            'name': name,
            'url': url,
            'price': price,
        }

        write_csv(file_name, data, labels)


# Get and send data to writer.
def main_writer(file_name, labels):
    url = 'https://coinmarketcap.com/'

    while True:
        # Get html
        html = get_html(url)

        # Parse data to csv file
        parse_and_send_to_write_data(file_name, html, labels)

        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            pattern = 'Next'
            regex = re.compile(pattern)

            # Get href from pagination
            pagination = soup.find('div', class_='cmc-table-listing__pagination')
            href = pagination.find('a', text=regex).get('href')

            # Change url
            url = 'https://coinmarketcap.com' + href
            print(url)
        except:
            print('End')
            break


# Read show data from csv file.
def main_reader(file_name, labels):
    read_csv(file_name, labels)


# Main.
def main():
    file_name = 'cmc.csv'

    labels = ['name', 'url', 'price']

    # Get, parse, write data
    main_writer(file_name, labels)

    # Read show data from csv file
    main_reader(file_name, labels)


if __name__ == '__main__':
    main()
