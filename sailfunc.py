import requests
from bs4 import BeautifulSoup
import csv

class GetSailboat:

  def __init__(self, city, query, min_price, max_price, seller='owner'):
      self.city = city
      self.query = query
      self.min_price = min_price
      self.max_price = max_price
      self.seller = seller
      self.boats_info = self.get_boats_info()

  # get search url
  def get_search_url(self):
    head = 'https://'
    tail = '.craigslist.org/search/sss'
    url = head + self.city + tail

    return url

  # create req object
  def get_results(self):
    payload = {
      'query': self.query,
      'min_price': self.min_price,
      'max_price': self.max_price,
      'data-val': self.seller,
      'sort': 'pricedsc'
    }

    url = self.get_search_url()
    r = requests.get(url, params=payload)
    s = BeautifulSoup(r.content, 'lxml')
    results = s.find_all('p', class_='result-info', limit=10)

    return results

  # parse through results:
  def get_boats_info(self):
    boats = []

    for result in self.get_results():
      try:
        area = (result.find('span', class_='result-hood').text.strip().strip('(').strip(')'))
      except AttributeError:
        area = ('Not displayed')
      title = (result.find('a', class_='result-title hdrlnk').text)
      price = (result.find('span', class_='result-price').text[1:])
      link = (result.find('a', class_='result-title hdrlnk')['href'])
      boats.append([self.city, area, title, price, link])

    return boats

def get_big_search(cities, query, min_price=5000, max_price=12000):
  search = []

  for city in cities:
    c = GetSailboat(city, query, min_price, max_price)
    search.append(c.boats_info)

  return search

def get_csv_file(search_list):

  with open('boat_search.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

    for city in search_list:
      for boat in city:
        csv_writer.writerow(boat)

