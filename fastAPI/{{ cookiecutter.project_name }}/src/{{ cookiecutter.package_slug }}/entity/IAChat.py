
from pydantic import BaseModel
from {{ cookiecutter.package_slug }}.entity.Entity import Entity
from {{ cookiecutter.package_slug }}.models.llm.GroqLLM import GroqLLM


class IAChatModel(BaseModel):
    message: str
    context: str = ""
    

class IAChat(Entity):
    
    def __init__(self):
        self.ia = GroqLLM()
    
    def load(self, chatmodel:IAChatModel):
        self.entity = self.to_json(chatmodel)
        self.__message = self.entity["message"]
        self.__context = self.entity["context"]
        
    def setMessage(self, message):
        self.__message = message
    def getMessage(self):
        return self.__message

    def setContext(self, context):
        self.__context = context
    def getContext(self):
        return self.__context
    
    def respond(self):
        resp = ""
        if self.__message:
            resp = self.ia.retrieve_message(self.__message, self.__context)
        return resp
            
    
    