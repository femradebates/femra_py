import json
from requests import request

class Definition:
    def __init__(self, defDict):
        self.term=defDict['term']
        self.notes=defDict['notes']
        self.prefix=defDict['prefix']
        self.altTerms=defDict['altTerms']
        self.definition=defDict['def']
    
    def __str__(self):
        """Returns the markdown of the definition"""
        return "placeholder"

class Definitions:
    def __init__(self,url):
        
        response=request("GET",url)
        if not response.ok:
            raise Exception("Failed to load definitions")
        defs=json.loads(response.text)
        self._glossary_={defDict['term']:Definition(defDict) for defDict in defs}
    
    def __getitem__(self,key):
        if not isinstance(key,str):
            raise TypeError("Expected string subscript, got {}".format(type(key)))
        return self._glossary_[key]

    def __iter__(self):
        for res in sorted(self._glossary_.values(), key=lambda d: d.term.lower()):
            yield res

    def __contains__(self, key):
        return key in self._glossary_