import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def currency_writer(data):
    try:
        with open('currencies.csv', 'w', newline='') as f:
            title = ['Код літерний', 'Кількість одиниць валюти', 'Назва валюти', 'Офіційний курс']
            file_writer = csv.writer(f, delimiter=";")
            file_writer.writerow(title)
            file_writer.writerows(data[0])
            file_writer.writerow(['На дату', data[1]])
            print('All data was written successfully!')
    except Exception:
        print('Failed to write currencies data!')
        return False


def parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        last_date = soup.find('span', attrs={'id': 'exchangeDate'}).text
        currency_data = soup.find('table', attrs={'id': 'exchangeRates'}).find('tbody').find_all('tr')
        return currency_data, last_date
    except Exception:
        print('Failed to parse currency data!')
        return False


def get_data(data):
    currency_data = []
    for element in data[0]:
        literal_cod = element.find('td', attrs={'data-label': 'Код літерний'}).text.strip()
        currency_quantity = element.find('td', attrs={'data-label': 'Кількість одиниць валюти'}).text.strip()
        currency_name = element.find('td', attrs={'class': 'value-name'}).find('a').text.strip()
        rate = element.find('td', attrs={'data-label': 'Офіційний курс'}).text.strip()
        currency_data.append([literal_cod, currency_quantity, currency_name, rate])
    return currency_data, data[1]


def main():
    url = 'https://bank.gov.ua/ua/markets/exchangerates'
    html = get_html(url)
    currency_data = parser(html)
    data = get_data(currency_data)
    currency_writer(data)


if __name__ == '__main__':
    main()