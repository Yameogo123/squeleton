
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
    
    def delete(self):
        if self.getId():
            return self.deleteFile(self.getId())
        return None
    
    def getByName(self):
        if self.__filename:
            return self.getFileByName(self.__filename)
        return None
    
    async def getById(self):
        if self.getId():
            return await self.getFileById(self.getId())
        return None
    
    def setFilename(self, filename):
        self.__filename = filename
    
    def getFilename(self):
        return self.__filename
    
    def getStreaming(self):
        if self.getId():
            file = self.getFileById(self.getId())
            image_stream = io.BytesIO(file.read())
            if image_stream:
                return StreamingResponse(image_stream, headers={"Content-Disposition": "inline"})
        return None
    
    def download(self):
        if self.getId():
            file_data = self.getFileById(self.getId())
            return StreamingResponse(
                file_data, media_type=file_data.content_type, 
                headers={"Content-Disposition": f"attachment; filename={file_data.filename}"}
            )
        return None
    
    async def deleteGroup(self, ids:List[str]):
        try:
            for _id in ids:
                await self.deleteFile(ObjectId(_id))
        except Exception as e:
            logger.error(f"erreur: {e}")

    
    async def deleteAllOfUser(self, userId):
        from med_backend.entity.User import User
        try:
            userMD = User()
            user = userMD.get_by_id(ObjectId(userId))
            profile = user.get("profil", "")
            if profile:
                return await self.deleteFile(profile)
            return None
        except Exception as e:
            logger.error(e)
            return None