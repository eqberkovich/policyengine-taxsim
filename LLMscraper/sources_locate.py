"""
Script to find datasources for SNAP
"""
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin, urlunsplit

sources = {
  "SNAP.COLA"              : "https://www.fns.usda.gov/snap/allotment/COLA"
, "SNAP.STATE_WEBSITES"    : "https://www.fns.usda.gov/snap/state-directory"
}

regions = [ 
  "48 States and District of Columbia"
#, "Alaska (Urban)"
#, "Alaska (Rural 1)"
#, "Alaska (Rural 2)"
, 'Alaska'
, "Guam"
, "Hawaii"
, "Virgin Islands"
]

state_names = [
  "Alabama",
  "Alaska",
  "Arizona",
  "Arkansas",
  "California",
  "Colorado",
  "Connecticut",
  "Delaware",
  "District of Columbia",
  "Florida",
  "Georgia",
  "Guam",
  "Hawaii",
  "Idaho",
  "Illinois",
  "Indiana",
  "Iowa",
  "Kansas",
  "Kentucky",
  "Louisiana",
  "Maine",
  "Maryland",
  "Massachusetts",
  "Michigan",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Montana",
  "Nebraska",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "New York City",
  "North Carolina",
  "North Dakota",
  "Ohio",
  "Oklahoma",
  "Oregon",
  "Pennsylvania",
  "Puerto Rico",
  "Rhode Island",
  "South Carolina",
  "South Dakota",
  "Tennessee",
  "Texas",
  "Utah",
  "Vermont",
  "Virgin Islands",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Wyoming"
]


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



if( __name__ == "__main__") :
  url = sources['SNAP.COLA']
  table_data = extract_data_sources(url)

  url = sources["SNAP.STATE_WEBSITES"]
  #data = extract_named_links( url, state_names )

  from extract_from_url import get_text_from_url, extract_parameter, Parameter
  url = table_data['Maximum Allotments and Deductions']['2023']
  print( url )
  text = get_text_from_url( url )
  d = 'The USDA deducts this amount from net income when computing SNAP benefits; the standard deduction.'
  p = Parameter(d, household_range=range(1,7), regions=regions)
  extract_parameter(text, p)
  for h in range(1,7):
    for r in range(len(regions)) :
      print( f"HH {h} in {regions[r]}: {p.values[(r,h)]}" )