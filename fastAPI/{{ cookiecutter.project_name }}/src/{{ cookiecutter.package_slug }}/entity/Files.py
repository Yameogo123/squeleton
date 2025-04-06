
from pydantic import BaseModel
from {{ cookiecutter.package_slug }}.entity.Entity import Entity
import io
from fastapi.responses import StreamingResponse

class DocumentModel(BaseModel):
    libelle: str
    description: str
    file_id: str = ""



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
                return StreamingResponse(image_stream)
        return None
    
    def download(self):
        if self.getId():
            file_data = self.getFileById(self.getId())
            return StreamingResponse(
                file_data, media_type=file_data.content_type, 
                headers={"Content-Disposition": f"attachment; filename={file_data.filename}"}
            )
        return None