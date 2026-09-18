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
    
    async def saveModel(self, document):
        return await make_crud_action(self.__model_name, "insert_one", document= document)
    
    async def saveAllModel(self, documents):
        return await make_crud_action(self.__model_name, "insert_many", documents= documents)
    
    async def updateModels(self, filter, update):
        return await make_crud_action(self.__model_name, "update_many", filter = filter, update = {"$set": update})

    async def updateModel(self, filter, update):
        return await make_crud_action(self.__model_name, "update_one", filter = filter, update = {"$set": update})
    
    async def pushUpdateModel(self, filter, update):
        return await make_crud_action(self.__model_name, "update_one", filter = filter, update = {"$addToSet": update})
    
    async def pullUpdateModel(self, filter, update):
        return await make_crud_action(self.__model_name, "update_one", filter = filter, update = {"$pull": update})
    
    async def deleteModel(self, filter):
        return await make_crud_action(self.__model_name, "delete_one", filter = filter)
    
    async def purgeModel(self, filter= {}):
        return await make_crud_action(self.__model_name, "purge", filter = filter)
    
    async def getModel(self, filter):
        res = await make_crud_action(self.__model_name, "find_one", filter = filter)
        return serialize_model(res) if res else None
    
    async def getModels(self):
        models = await make_crud_action(self.__model_name, "find_all")
        return [serialize_model(x) for x in models]
    
    async def getModelsBy(self, filter):
        models = await make_crud_action(self.__model_name, "find_all", filter = filter)
        return [serialize_model(x) for x in models]
    
    def to_json(self, model):
        return serialize_model(from_model_to_dict(model))
    
    def setId(self, id):
        self.__id = id
    
    def getId(self):
        return self.__id
    
    ######### file
    async def getFileByName(self, name:str):
        return await handle_file("find_one", filename=name)
    
    async def getFileById(self, id):
        return await handle_file("find_one", id=id)
    
    async def newFile(self, file):
        file_content = await file.read()
        return await handle_file("insert_one", file=file, file_content=file_content)
    
    async def deleteFile(self, id):
        return await handle_file("delete_one", id=id)