"""
Scripts to build yaml parameter files
"""
from extract_from_url import get_text_from_url, extract_parameter, extract_parameter_from_csv, Parameter
from sources_locate import extract_data_sources

sources = {
  "SNAP.COLA"                   : "https://www.fns.usda.gov/snap/allotment/COLA"
, "SNAP.STATE_WEBSITES"         : "https://www.fns.usda.gov/snap/state-directory"
, "SNAP.UTILITY_ALLOWANCE.2024" : "https://www.fns.usda.gov/sites/default/files/resource-files/snap-sua-table-fy24-032624.xlsx"
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



def build_utility_allowance() :
  """
  Make yaml file for standard utility allowance
  """
  data = get_text_from_url( sources["SNAP.UTILITY_ALLOWANCE.2024"] )
  d = 'The Heating and Cooling Standard Utility Allowance (HCSUA) for SNAP households.'
  p = Parameter(d, household_range=None, regions=state_names)
  extract_parameter_from_csv(data, p)
  print( p.values )


build_utility_allowance()
if( __name__ == "__main__") :
  exit
  url = sources['SNAP.COLA']
  table_data = extract_data_sources(url)

  section_name = 'Maximum Allotments and Deductions'
  years_range  = range(2020, 2025)

  for year in years_range :
    url = table_data[section_name][year]
    print( url )
    text = get_text_from_url( url )
    d = 'The USDA deducts this amount from net income when computing SNAP benefits; the standard deduction.'
    p = Parameter(d, household_range=range(1,7), regions=regions)
    extract_parameter(text, p)
  for h in range(1,7):
    for r in range(len(regions)) :
      print( f"HH {h} in {regions[r]}: {p.values[(r,h)]}" )