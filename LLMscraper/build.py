"""
Scripts to build yaml parameter files
"""
import yaml
import datetime
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
location_codes = {
    "Alabama"             : "AL",
    "Alaska"              : "AK",
    "Arizona"             : "AZ",
    "Arkansas"            : "AR",
    "California"          : "CA",
    "Colorado"            : "CO",
    "Connecticut"         : "CT",
    "Delaware"            : "DE",
    "District of Columbia": "DC",
    "Florida"             : "FL",
    "Georgia"             : "GA",
    "Guam"                : "GU",  
    "Hawaii"              : "HI",
    "Idaho"               : "ID",
    "Illinois"            : "IL",
    "Indiana"             : "IN",
    "Iowa"                : "IA",
    "Kansas"              : "KS",
    "Kentucky"            : "KY",
    "Louisiana"           : "LA",
    "Maine"               : "ME",
    "Maryland"            : "MD",
    "Massachusetts"       : "MA",
    "Michigan"            : "MI",
    "Minnesota"           : "MN",
    "Mississippi"         : "MS",
    "Missouri"            : "MO",
    "Montana"             : "MT",
    "Nebraska"            : "NE",
    "Nevada"              : "NV",
    "New Hampshire"       : "NH",
    "New Jersey"          : "NJ",
    "New Mexico"          : "NM",
    "New York"            : "NY",
    "New York City"       : "NYC",
    "North Carolina"      : "NC",
    "North Dakota"        : "ND",
    "Ohio"                : "OH",
    "Oklahoma"            : "OK",
    "Oregon"              : "OR",
    "Pennsylvania"        : "PA",
    "Puerto Rico"         : "PR",  
    "Rhode Island"        : "RI",
    "South Carolina"      : "SC",
    "South Dakota"        : "SD",
    "Tennessee"           : "TN",
    "Texas"               : "TX",
    "Utah"                : "UT",
    "Vermont"             : "VT",
    "Virgin Islands"      : "VI",  
    "Virginia"            : "VA",
    "Washington"          : "WA",
    "West Virginia"       : "WV",
    "Wisconsin"           : "WI",
    "Wyoming"             : "WY"
}

def _find_location_name( location_code : str ) -> str :
  location_code = location_code.lower()
  for key, val in location_codes.items() :
    if( val.lower() == location_code ) :
      return key
  return None


def build_utility_allowance( input_yaml_file : str ) -> dict :
  """
  Make yaml file for standard utility allowance
  Args:
    input_yaml_file     : Filename of SNAP utility allowances YAML
  Returns:
    dict of new YAML
  """
  with open(input_yaml_file, 'r') as f:
    yaml_data = yaml.safe_load(f.read()) 

  # Ideally this description would be in input YAML
  description = 'The Heating and Cooling Standard Utility Allowance (HCSUA) for SNAP households.'
  
  # Locate the new source of info and fetch it
  p    = Parameter(description, household_range=None, regions=list(location_codes.keys()))
  data = get_text_from_url( sources["SNAP.UTILITY_ALLOWANCE.2024"] )
  extract_parameter_from_csv(data, p)
  
  # Update the YAML
  # Has state codes at base level
  for k in yaml_data.keys() :
    if( location_name := _find_location_name( k ) ):
      new_date = datetime.date(2024, 10, 1)  # TBD: Get active date from file
      # Overwrite if needed
      yaml_data[k][new_date] = p.get_value(household_size=None, region=location_name)

  return yaml_data


def build_allotments() :
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


if( __name__ == '__main__') :

  SUA_yaml = 'D:\\PolicyEngine\\code\\policyengine_us\\parameters\\gov\\usda\\snap\\income\\deductions\\utility\\standard.yaml'
  new_yaml = build_utility_allowance( SUA_yaml )
