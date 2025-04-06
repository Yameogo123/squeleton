

class LLM:
    
    def __init__(self):
        pass
    
    def setAPIKey(self, api:str):
        self.__api_key = api
        
    def getAPIKey(self):
        return self.__api_key
    
    def setModelName(self, name):
        self.__model_name = name
    
    def getModelName(self):
        return self.__model_name
    
    def setSystemPrompt(self, system_prompt):
        self.__system_prompt = system_prompt
        
    def getSystemPrompt(self):
        return self.__system_prompt
    
    def setUserPrompt(self, user_prompt):
        self.__user_prompt = user_prompt
    
    def getUserPrompt(self):
        return self.__user_prompt