import requests


# Get html from url.
def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


# Main
def main():
    url = 'https://coinmarketcap.com/'

    html = get_html(url)


if __name__ == '__main__':
    main()
