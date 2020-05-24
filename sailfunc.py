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

  # return search url from city name
  def get_search_url(self):
    head = 'https://'
    tail = '.craigslist.org/search/sss'
    url = head + self.city + tail

    return url

  # return soup object for parsing results (10 results max)
  def get_results(self):
    payload = {
      'query': self.query,
      'min_price': self.min_price,
      'max_price': self.max_price,
      'data-val': self.seller,
      'sort': 'pricedsc'
    }

    url = self.get_search_url()
    r = requests.get(url, params=payload) # .get request object to perform search
    s = BeautifulSoup(r.content, 'lxml') # soup object from search page content
    results = s.find_all('p', class_='result-info', limit=10) # finds results tag, limits to 10 results

    return results

  # return list of relevant info from soup object
  def get_boats_info(self):
    boats = []

    for result in self.get_results():
      
      # deal with area not being available in all results
      try:
        area = (result.find('span', class_='result-hood').text.strip().strip('(').strip(')'))
      except AttributeError:
        area = ('Not displayed')
      
      # get listing title, price and link
      title = (result.find('a', class_='result-title hdrlnk').text)
      price = (result.find('span', class_='result-price').text[1:])
      link = (result.find('a', class_='result-title hdrlnk')['href'])
      boats.append([self.city, area, title, price, link])

    return boats

# iterate through list of cities
# return list of lists of results
def get_big_search(cities, query, min_price=5000, max_price=12000):
  search = []

  for city in cities:
    c = GetSailboat(city, query, min_price, max_price)
    search.append(c.boats_info)

  return search

# dump list to csv file
def get_csv_file(search_list):

  with open('boat_search.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

    for city in search_list:
      for boat in city:
        csv_writer.writerow(boat)

