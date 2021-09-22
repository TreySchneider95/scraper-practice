import csv
from bs4 import BeautifulSoup
import requests

# URL to the website
URL = 'http://quotes.toscrape.com/tableful'

# Getting the html file and parsing with html.parser
html = requests.get(URL)
bs = BeautifulSoup(html.text, 'html.parser')

# Tries to open the file
try:
    csv_file = open('quote_list.csv', 'w')
    fieldnames = ['quote', 'author', 'tags']
    dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Writes the headers
    dictwriter.writeheader()

    # While next button is found in the page the loop runs
    while True:
        dict = {}
        tag_counter = 0
        quote_counter = 0
        for foo in bs.findAll('td', {'style': 'padding-bottom: 2em;'}):
            tags = []
            for tag in foo.findAll('a'):
                tags.append(tag.text)
            dict[tag_counter]=tags
            tag_counter += 1
        # Loops through quote in the page
        for quote in bs.findAll('tr', {'style': 'border-bottom: 0px; '}):
            # Extract the text part of quote, author and tags
            text = quote.find('td', {'style': 'padding-top: 2em;'}).text
            lst = text.split(' Author: ')
            text = lst[0]
            author = lst[1]
            # print(7)
            # print(9)
            # Writes the current quote,author and tags to a csv file
            dictwriter.writerow(
                {'quote': text, 'author': author, 'tags': dict[quote_counter]})
            quote_counter += 1
                # {'quote': text, 'author': author})

        # Finds the link to next page
        next = [(x.text, x['href']) for x in bs.find_all('a')if 'Next \n                    ' in x.text]
        if len(next) == 0:
            break

        # Gets and parses the html file of next page
        html = requests.get(URL+next[0][1][9:])
        bs = BeautifulSoup(html.text, 'html.parser')
except:
    print('Unknown Error!!!')
finally:
    csv_file.close()
