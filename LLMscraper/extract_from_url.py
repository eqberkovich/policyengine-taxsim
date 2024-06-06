"""
Script to scrape parameters
"""
from LLMAccessor import LLMAccessor
import requests

class Parameter():
    name        : str
    description : str



def extract_parameter( url : str, param : Parameter )  :
    request = requests.get( url )
    text    = request.content
    prompt  = f"Find the value of parameter which is defined as: {param.description} " \
            + f" \n\n The following context contains the needed information: \n {text}"
    
    llm    = LLMAccessor()
    answer = llm.generate( prompt )

    return answer


if( __name__ == "__main__" ) :
    url = "https://www.pa.gov/en/agencies/dhs/resources/snap/snap-income-limits.html"
    p = Parameter()
    p.name = "IncomeLimit2"
    p.description = "The maximum gross monthly income for a family of 2 to be eligible for SNAP benefits."
    a = extract_parameter( url, p )
    print( a )