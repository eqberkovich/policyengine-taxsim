"""
Script to scrape parameters
"""
from LLMAccessor import LLMAccessor
import requests
from bs4 import BeautifulSoup 
import yaml
import pathlib

yaml_files = [
    "D:\\PolicyEngine\\code\\policyengine_us\\parameters\\gov\\usda\\snap\\income\\deductions\\earned_income.yaml"
,   "D:\\PolicyEngine\\code\\policyengine_us\\parameters\\gov\\usda\\snap\\min_allotment\\rate.yaml"
]


def get_text_from_url( url : str ) -> str :
    request = requests.get( url )
    # TBD: Handle PDF files, other formats?
    bs      = BeautifulSoup( request.content, features="html.parser" )
    text    = bs.get_text()
    return text

def extract_parameter( text : str, param_description : str ) -> float  :
    """
    Given text data, ask the LLM to look for numerical values which correspond
    to the description of the parameter. 
    Parameters
        text                : Text to parse for parameter value
        param_description   : Detailed description of the numerical value to find
    Returns:
        float value of the parameter or None if not found
    """
    
    prompt  = f"Find the value of parameter which is defined as: {param_description} " \
            + f" \n Write your answer as python code using 'param_1' as the variable. " \
            + f" \n\n The following context contains the needed information: \n {text}"
    
    llm    = LLMAccessor()
    answer = llm.generate( prompt )

    lines = answer.splitlines()
    val   = None
    for line in lines :
        i = line.find('=')
        if( i > 0 ) :
            val = float(line[i+1:])
    return val


def read_yaml( filename : str | pathlib.Path ) :
    with pathlib.Path(filename).open('r') as file:
        data = yaml.safe_load(file)
    return data


if( __name__ == "__main__" ) :
    for file in yaml_files :
        data = read_yaml( pathlib.Path(file) )
        
        url         = data['metadata']['reference'][0]['href']
        description = data['description']
        values      = data['values']  
        # last value is the one to compare to
        value = values[max(values, key=values.get)]
        
        text = get_text_from_url( url )
        a    = extract_parameter( text, description )
        print( f"{description}: {a}" )
        if( a != value ) :
            print( f" NO MATCH! Previous value was {value}. ")

        

