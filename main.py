import requests
import json
from bs4 import BeautifulSoup


BASE_URL = 'http://quotes.toscrape.com/'


def parse_page(soup, authors_name):

    quotes = soup.find_all('div', {'class': 'quote'})
    all_quote = []
    all_author = []

    for quote in quotes:
        author_name = quote.find('small', {'class': 'author'}).get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', {'class': 'tag'})]
        quote_text = quote.find('span', {'class': 'text'}).get_text()
        author_url = BASE_URL + quote.find('a')['href']
        all_quote.append({'tags': tags, 'author': author_name, 'quote': quote_text})

        if author_name not in authors_name:

            response = requests.get(author_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            born_date = soup.find('span', {'class': 'author-born-date'}).get_text()
            born_location = soup.find('span', {'class': 'author-born-location'}).get_text()
            description = soup.find('div', {'class': 'author-description'}).get_text().strip()
            all_author.append({'fullname': author_name, 'born_date': born_date,
                               'born_location': born_location, 'description': description})

        authors_name.add(author_name)

    return authors_name, all_quote, all_author


def main():

    all_quotes = []
    all_authors = []
    all_authors_name = set()
    num_page = 1

    while True:

        print(f'Scraping page #{num_page}')
        next_page = f'{BASE_URL}/page/{num_page}/'
        response = requests.get(next_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_authors_name, quotes, authors = parse_page(soup, all_authors_name)
        all_quotes = all_quotes + quotes
        all_authors = all_authors + authors

        if soup.find('li', {'class': 'next'}):
            num_page += 1
        else:
            break

    with open('quotes.json', 'w') as file:
        json.dump(all_quotes, file, indent=2)

    with open('authors.json', 'w') as file:
        json.dump(all_authors, file, indent=2)


if __name__ == "__main__":
    main()
