"""
Script to find datasources for SNAP
"""
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin, urlunsplit

def _make_full_URL( url : str, base_url : str ) -> str :
  if ( url.startswith('http://') or url.startswith('https://')) :
    return url
  else :
    base_parsed = urlparse(base_url)
    new_url     = urlunsplit((base_parsed.scheme, base_parsed.netloc, "", "", ""))
    new_url     = urljoin(new_url, url)
    return new_url
   

def extract_data_sources(url : str) -> dict :
  """
  Extracts table data from a webpage. Assumes tables have 
  titles immediately preceding.

  Args:
      url: The URL of the webpage.

  Returns:
      A dictionary with table titles as keys and nested dictionaries with year-URL pairs.
  """
  data     = {}
  response = requests.get(url)
  soup     = BeautifulSoup(response.content, 'html.parser')

  # Find all potential table titles (siblings preceding tables)
  potential_tables = soup.find_all('table')
  for t in potential_tables:
    title           = t.previous_sibling
    title_key       = title.text
    data[title_key] = {}  
    for row in t.find_all('tr'):
      for cell in row.find_all('td'):
        link = cell.find('a', href=True)
        if link:
          year    = link.text.strip()
          pdf_url = link['href']

          data[title_key][year] = _make_full_URL( pdf_url, url)

  return data


def extract_named_links(url : str, sources : list, ignorecase : bool = True ) -> dict :
  """
  Compiles list of URLs from a page. Assumes given sources are links.

  Args:
      url: The URL of the webpage.
      sources: List of strings to find on webpage. Assumes each name is a link.

  Returns:
      A dictionary with source-URL pairs.
  """
  data     = {}
  response = requests.get(url)
  soup     = BeautifulSoup(response.content, 'html.parser')

  if( ignorecase ) :
    sources = [s.lower() for s in sources]

  for a_tag in soup.find_all('a'):  # Find all anchor tags
    text = a_tag.text.strip()  
    if( ignorecase ) :
      text = text.lower()

    if text in sources:  
      a_url      = a_tag.get('href')  
      data[text] = _make_full_URL(a_url, url)

  return data

