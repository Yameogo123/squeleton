from {{ cookiecutter.package_slug }}.entity.Entity import Entity
import io
from bson.objectid import ObjectId
from fastapi.responses import StreamingResponse
from loguru import logger
from typing import List



class Files(Entity):
    
    def __init__(self, file = None):
        self.__file = file
    
    def load(self, file):
        self.__file = file
    
    async def save(self):
        if self.__file:
            return await self.newFile(self.__file)
        return None
    
    async def delete(self):
        if self.getId():
            return await self.deleteFile(self.getId())
        return None
    
    async def getByName(self):
        if self.__filename:
            return await self.getFileByName(self.__filename)
        return None
    
    async def getById(self):
        if self.getId():
            return await self.getFileById(self.getId())
        return None
    
    def setFilename(self, filename):
        self.__filename = filename
    
    def getFilename(self):
        return self.__filename
    
    async def getStreaming(self):
        if self.getId():
            file = await self.getFileById(self.getId())
            if file:
                file_content = await file.read()
                image_stream = io.BytesIO(file_content)
                if image_stream:
                    return StreamingResponse(image_stream, headers={"Content-Disposition": "inline"})
        return None
    
    async def download(self):
        if self.getId():
            file_data = await self.getFileById(self.getId())
            if file_data:
                file_content = await file_data.read()
                return StreamingResponse(
                    io.BytesIO(file_content), media_type=file_data.content_type, 
                    headers={"Content-Disposition": f"attachment; filename={file_data.filename}"}
                )
        return None
    
    async def deleteGroup(self, ids:List[str]):
        try:
            for _id in ids:
                await self.deleteFile(ObjectId(_id))
        except Exception as e:
            logger.error(f"erreur: {e}")