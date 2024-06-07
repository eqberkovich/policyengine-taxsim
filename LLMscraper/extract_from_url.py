"""
Script to scrape parameters
"""
from LLMAccessor import LLMAccessor
import requests
from bs4 import BeautifulSoup 


def extract_parameter( url : str, param_description : str ) -> float  :
    request = requests.get( url )
    bs      = BeautifulSoup( request.content, features="html.parser" )
    text    = bs.get_text()
    
    prompt  = f"Find the value of parameter which is defined as: {param_description} " \
            + f" \n Write your answer as python code using 'param_1' as the variable. " \
            + f" \n\n The following context contains the needed information: \n {text}"
    
    llm    = LLMAccessor()
    answer = llm.generate( prompt )

    lines = answer.splitlines()
    for line in lines :
        i = line.find('=')
        if( i > 0 ) :
            x = float(line[i+1:])
    return x


if( __name__ == "__main__" ) :
    url = "https://www.pa.gov/en/agencies/dhs/resources/snap/snap-income-limits.html"
    description = "The maximum gross monthly income for a family of 2 to be eligible for SNAP benefits."
    #a = extract_parameter( url, description )

    url = "https://www.law.cornell.edu/uscode/text/7/2014#e_5"
    description = "Monthly medical expenses disregarded for claiming SNAP excess medical expense deduction"
    a = extract_parameter( url, description )
    print( a )
    assert( a == 35 )