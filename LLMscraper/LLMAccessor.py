"""
Connector to LLM
"""
import google.generativeai as genai
import tomllib

class LLMAccessor() :

    def __init__( self ) :
        with open('.secrets/apikeys.toml', 'rb') as f:
            secrets = tomllib.load(f)
        self.api_key = secrets['apikey']

        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

        # Max size of model attention window in bytes (should be in tokens, so assuming 5 byte words)
        #   Note: Gemini Pro 1.5 is 1m tokens; 1.0 is 150k (?)
        self._size_window = 500000 * 5    


    def generate( self, prompt ) -> str :
        prompt   = prompt[:self._size_window]
        response = self._model.generate_content( prompt )
        return response.text



# TEST code  
if( __name__ == '__main__')  :

    print( 'Starting...' )

    llm = LLMAccessor( )
    answer = llm.generate('Tell me a story about a rabbit.')

    print( f"ANSWER: \n {answer}" )
