"""
Script to scrape parameters
"""
from LLMAccessor import LLMAccessor
import requests
from bs4 import BeautifulSoup 
from PyPDF2 import PdfReader
from io import BytesIO


class Parameter() :

    def __init__(  self
                 , description : str 
                 , years_range : range = None
                 , regions     : list  = None) :
        """
        Initialize the Parameter description
        """
        self.description = description
        self.has_regions = (regions != None)
        self.has_years   = (years_range != None)
        self.years_range = years_range
        self.regions     = regions
        
        keys = list()
        if( self.has_regions and self.has_years ) :
            for r in regions :
                for year in years_range :
                    keys.append( (r, year) )
        elif( self.has_regions ) :
            for r in regions :
                keys.append( r )
        elif( self.has_years ) :
            for year in years_range :
                keys.append( year )
        else :
            keys.append( None )
        
        values = dict()
        for k in keys:        
            values[k] = None


    def set_value(self, value : float, year : int = None, region : str = None ):
        if( self.has_years and self.has_regions ) :
            self.values[(region, year)] = value
        elif( self.has_years ) :
            self.values[year] = value
        elif( self.has_regions ) :
            self.values[region] = value
        else :
            self.values[None] = value


def get_text_from_url( url : str ) -> str :
    """
    Fetch plain text from a URL which has format as HTML or a PDF 
    Parameters:
        url     : The URL to get text from
    Returns:
        Plain text of the contents
    """
    request = requests.get( url )
    # TBD -- Handle errors more gracefully

    text = ""
    if( ".pdf" in url.lower() ) :
        with BytesIO(request.content) as pdf_data :
            pdf_reader = PdfReader(pdf_data)
            for page in pdf_reader.pages:
                text += page.extract_text()
    else :
        bs   = BeautifulSoup( request.content, features="html.parser" )
        text = bs.get_text()

    return text


def extract_parameter( text : str, param : Parameter ) -> dict  :
    """
    Given text data, ask the LLM to look for numerical values which correspond
    to the description of the parameter. 
    Parameters
        text    : Text to parse for parameter value
        param   : Parameter object with detailed description of the numerical values to find
    Returns:
        dictionary of the parameter or None if not found
    """

    prompt  = f"Find the value of parameter which is defined as: {param.description} " \
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

