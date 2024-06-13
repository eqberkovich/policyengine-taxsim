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
                 , description     : str 
                 , household_range : range = None
                 , regions         : list  = None) :
        """
        Initialize the Parameter description
        """
        self.description    = description
        self.has_regions    = (regions != None)
        self.has_HH         = (household_range != None)
        self.HH_range       = household_range
        self.regions        = regions
        self.regions_range  = range(len(regions))
        
        keys = list()
        if( self.has_regions and self.has_HH ) :
            for r in self.regions_range :
                for h in household_range :
                    keys.append( (r, h) )
        elif( self.has_regions ) :
            for r in self.regions_range :
                keys.append( r )
        elif( self.has_HH ) :
            for h in household_range :
                keys.append( h )
        else :
            keys.append( None )
        
        values = dict()
        for k in keys:        
            values[k] = None
        self.values = values


    def set_value(self, value : float, household_size : int = None, region_num : int = None ):
        if( self.has_HH and self.has_regions ) :
            key = (region_num, household_size)
        elif( self.has_HH ) :
            key = household_size
        elif( self.has_regions ) :
            key = region_num
        else :
            key = None
        
        if( key in self.values.keys()) :
            self.values[key] = value
        else :
            raise( KeyError(f"Cannot set the parameter value for {key}. Outside of allowed ranges."))

# end Parameter class


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


def extract_parameter( text : str, param : Parameter ) -> None  :
    """
    Given text data, ask the LLM to look for numerical values which correspond
    to the description of the parameter. 
    Parameters
        text    : Text to parse for parameter value
        param   : Parameter object with detailed description of the numerical values to find
                  This object gets filled in with data
    Returns:
        None
    """

    prompt  = f"Using the attached context, find the value of parameter which is defined as: {param.description} " \
                + "\n Write your answer entirely as python code. No comments. No other text.\n "
    prompt += "Find the value "
    if( param.has_HH ) :
        prompt += " for each household size"
    if( param.has_regions ) :
        prompt += " for each region"
    prompt +=". Write each parameter as a the example code: param"
    if( param.has_HH ) :
        prompt += "_H"
    if( param.has_regions) :
        prompt += "_R"
    prompt += "=VALUE \n where VALUE is the parameter value "
    if( param.has_HH ) :
        prompt += " and H is the household size "
    if( param.has_regions) :
        prompt += " and R is the region number mapped as "
        for r in range(len(param.regions)) :
            prompt += f" {r} is '{param.regions[r]}', "
    prompt += f"\n The contexts is:\n\n {text}"
    has_regions_HH = (param.has_HH and param.has_regions)

    llm    = LLMAccessor()
    answer = llm.generate( prompt )

    def parse_varname( v : str ) :
        parts = v.split('_')
        x     = list()
        for p in parts :
            x.append(float(p))
        return x

    lines = answer.splitlines()
    val   = None
    for line in lines :
        i = line.find('=')
        if( i > 0 ) :
            v   = line[i+1:]
            # LLM sometimes adds comments 
            c   = v.find('#')
            if( c > 0 ) :
                v = v[:c]
            val = float(v)
            ids = line[:i].split('_')

            household_size = None
            region_num     = None
            if( has_regions_HH ) :
                household_size = int(ids[1])
                region_num     = int(ids[2])
            elif( param.has_HH ) :
                household_size = int(ids[1])
            elif( param.has_regions ) :
                region_num     = int(ids[1])
            try :
                param.set_value( val, household_size, region_num )
            except Exception as e:
                print( e )

    return 

