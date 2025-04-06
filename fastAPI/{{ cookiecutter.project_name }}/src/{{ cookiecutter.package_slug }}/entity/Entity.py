

from {{ cookiecutter.package_slug }}.data.mongodb import (
    make_crud_action, handle_file
)
from {{ cookiecutter.package_slug }}.utils.controller import (
    from_model_to_dict, serialize_model
)

class Entity:
    
    def __init__(self, model_name:str):
        self.__model_name = model_name
    
    def getModelName(self):
        return self.__model_name
    
    def setModelName(self, model_name):
        self.__model_name = model_name
    
    def saveModel(self, document):
        return make_crud_action(self.__model_name, "insert_one", document= document)
    
    def updateModel(self, filter, update):
        return make_crud_action(self.__model_name, "update_one", filter = filter, update = {"$set": update})
    
    def deleteModel(self, filter):
        return make_crud_action(self.__model_name, "delete_one", filter = filter)
    
    def getModel(self, filter):
        return serialize_model(make_crud_action(self.__model_name, "find_one", filter = filter))
    
    def getModels(self):
        return [serialize_model(x) for x in make_crud_action(self.__model_name, "find_all").to_list()]
    
    def getModelsBy(self, filter):
        return [serialize_model(x) for x in make_crud_action(self.__model_name, "find_all", filter = filter).to_list()]
    
    def to_json(self, model):
        return serialize_model(from_model_to_dict(model))
    
    def setId(self, id):
        self.__id = id
    
    def getId(self):
        return self.__id
    
    ######### file
    def getFileByName(self, name:str):
        return handle_file("find_one", filename=name)
    
    def getFileById(self, id):
        return handle_file("find_one", id=id)
    
    async def newFile(self, file):
        file_content = await file.read()
        return handle_file("insert_one", file=file, file_content=file_content)
    
    async def deleteFile(self, id):
        return handle_file("delete_one", id=id)