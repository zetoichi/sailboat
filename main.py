"""
- Check Craigslist (West Coast) for:
  - query: 'sailboat'
  - min_price: 8000
  - max_price: 20000

- Get: city, area, name, price, link.

- Dump info to CSV

- Send e-mail notice

- Schedule weekly
"""
import sailfunc
import sailmail
import schedule
import time
from secrets import gmail_at, gmail_pass # secret login variables

# query variables
sailboat_query = 'sailboat'
west_coast_cities = ['vancouver', 'seattle', 'sfbay', 'losangeles', 'sandiego']
min_price = 8000
max_price = 20000

# e-mail server variables
gmail_smtp = 'smtp.gmail.com'
gmail_port = 465
sender = gmail_at
receiver = gmail_at
password = gmail_pass

# e-mail message variables
subject = 'SAILBOATS!'
body = 'These are the sailboats we found for you on Craigslist this week!'
attachment = '/Users/Zeta/CODE/PROJECTS/PYTHON/SAILBOAT/boat_search.csv'

def main():
  global west_coast_cities, sailboat_query
  global subject, body, attachment, gmail_smtp, gmail_port, sender, receiver, password, msg

  search_list = sailfunc.get_big_search(west_coast_cities, sailboat_query, min_price, max_price)
  sailfunc.get_csv_file(search_list)

  msg = sailmail.get_message(subject, body, attachment, sender, receiver)
  sailmail.send_mail(gmail_smtp, sender, receiver, password, msg)

# schedule to run weekly
schedule.every().monday.at('10:00').do(main)

while True:
  schedule.run_pending()
  time.sleep(1)