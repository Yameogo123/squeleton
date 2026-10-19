from {{ cookiecutter.package_slug }}.data.database import file_delete, file_read, file_upload, make_crud_action
from {{ cookiecutter.package_slug }}.utils.controller import from_model_to_dict, serialize_model


class Entity:
    """Base class: CRUD helpers bound to one table/collection.

    Return values are driver independent: save -> id (str), get -> dict | None,
    update/delete -> number of affected rows (int).
    """

    def __init__(self, model_name: str):
        self.__model_name = model_name
        self.__id = None

    def getModelName(self):
        return self.__model_name

    def setModelName(self, model_name):
        self.__model_name = model_name

    async def saveModel(self, document):
        return await make_crud_action(self.__model_name, "insert_one", document=document)

    async def saveAllModel(self, documents):
        return await make_crud_action(self.__model_name, "insert_many", documents=documents)

    async def updateModels(self, filter, update):
{%- if cookiecutter.database == 'mongodb' %}
        return await make_crud_action(self.__model_name, "update_many", filter=filter, update={"$set": update})
{%- elif cookiecutter.database == 'supabase' %}
        return await make_crud_action(self.__model_name, "update_many", filter=filter, update=update)
{%- endif %}

    async def updateModel(self, filter, update):
{%- if cookiecutter.database == 'mongodb' %}
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update={"$set": update})
{%- elif cookiecutter.database == 'supabase' %}
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update=update)
{%- endif %}

    async def pushUpdateModel(self, filter, update):
{%- if cookiecutter.database == 'mongodb' %}
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update={"$addToSet": update})
{%- elif cookiecutter.database == 'supabase' %}
        # Postgres arrays: prefer an RPC (array_append) for atomic appends
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update=update)
{%- endif %}

    async def pullUpdateModel(self, filter, update):
{%- if cookiecutter.database == 'mongodb' %}
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update={"$pull": update})
{%- elif cookiecutter.database == 'supabase' %}
        return await make_crud_action(self.__model_name, "update_one", filter=filter, update=update)
{%- endif %}

    async def deleteModel(self, filter):
        return await make_crud_action(self.__model_name, "delete_one", filter=filter)

    async def purgeModel(self, filter=None):
        return await make_crud_action(self.__model_name, "purge", filter=filter or {})

    async def getModel(self, filter):
        res = await make_crud_action(self.__model_name, "find_one", filter=filter)
        return serialize_model(res) if res else None

    async def getModels(self, limit: int = 0, skip: int = 0):
        models = await make_crud_action(self.__model_name, "find_all", limit=limit, skip=skip)
        return [serialize_model(x) for x in models]

    async def getModelsBy(self, filter, limit: int = 0, skip: int = 0):
        models = await make_crud_action(self.__model_name, "find_all", filter=filter, limit=limit, skip=skip)
        return [serialize_model(x) for x in models]

    def to_json(self, model):
        return serialize_model(from_model_to_dict(model))

    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    ######### file
    async def getFileById(self, id):
        return await file_read(str(id))

    async def newFile(self, filename: str, content: bytes, content_type: str):
        return await file_upload(filename, content, content_type)

    async def deleteFile(self, id):
        return await file_delete(str(id))
