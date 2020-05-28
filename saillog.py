"""
Basic decorator function that logs when key functions in the program are executed.

CHECK: add a logger specially for exceptions?
"""

import logging
from functools import wraps

# General logger decorator
def logger(f):

  logger = logging.getLogger(f.__name__)
  logger.setLevel(logging.INFO)

  formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

  file_handler = logging.FileHandler('saillog.log')
  file_handler.setFormatter(formatter)

  logger.addHandler(file_handler)

  @wraps(f)
  def wrapper(*a, **kw):

    if f.__name__ == 'try_csv':
      logger.info('CSV File created successfully')

    elif f.__name__ == 'try_mail':
      logger.info('E-mail sent successfully')
    
    else:
      logger.info('{} ran successfully'.format(f.__name__))
    
    return f(*a, *kw)
  
  return wrapper