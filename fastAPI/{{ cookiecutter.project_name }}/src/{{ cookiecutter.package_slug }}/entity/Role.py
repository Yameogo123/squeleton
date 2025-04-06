
from pydantic import BaseModel
from {{ cookiecutter.package_slug }}.entity.Entity import Entity

class RoleModel(BaseModel):
    libelle: str


class Role(Entity):
    
    def __init__(self, libelle:str = ""):
        super().__init__("role")
        self.__libelle = libelle
        
    def load(self, role: RoleModel):
        self.role = self.to_json(role)
        self.__libelle = self.role["libelle"]
    
    def save(self):
        if self.role:
            return self.saveModel(self.role)
        return None
    
    def update(self):
        if self.getId() and self.__libelle:
            return self.updateModel({"_id": self.getId()}, {"libelle": self.__libelle})
        else:
            return None
    
    def getOne(self, id):
        model =  self.getModel({"_id": id})
        return model
    
    def getAll(self):
        models = self.getModels()
        return models
    
    def delete(self):
        if self.getId():
            return self.deleteModel({"_id": self.getId()})
        return None
    
    def setLibelle(self, libelle):
        self.__libelle = libelle
    
    def getLibelle(self):
        return self.__libelle
    
    
