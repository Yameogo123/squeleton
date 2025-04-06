
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from {{ cookiecutter.package_slug }}.entity.Entity import Entity
from {{ cookiecutter.package_slug }}.utils.controller import hash_pwd, verify_password


class UserModel(BaseModel):
    nom: str = ""
    prenom : str = ""
    email: EmailStr = ""
    tel: str = ""
    password: str = ""
    role_id: str = ""
    specialite_id: str = ""
    cabinet_id: str = ""
    profil: str = ""
     


class User(Entity):
    
    def __init__(
        self, nom:str="", prenom:str="", email:EmailStr="", password:str=""
    ):
        super().__init__("user")
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__password = password

    
    def load(self, entite: UserModel):
        self.entite = self.to_json(entite)
        self.__nom = self.entite["nom"]
        self.__prenom = self.entite["prenom"]
        self.__email = self.entite["email"]
        self.__password = self.entite["password"]
    
    def save(self):
        if self.entite:
            if self.validate_password(self.entite["password"]):
                self.entite["password"] = hash_pwd(self.entite["password"])
                return self.saveModel(self.entite)
        return None
    
    def delete(self):
        if self.getId() :
            return self.deleteModel({"_id": self.getId()})
        return None
    
    def update(self):
        updt = {"nom": self.__nom, "prenom": self.__prenom}
        isValid = all(updt.values())
        if self.getId() and isValid:
            return self.updateModel({"_id": self.getId()}, updt)
        else:
            return None
    
    def get_by_id(self, id):
        return self.getModel({"_id": id})
    
    def getAll(self):
        models = self.getModels()
        return models
    
    def login(self):
        user = self.getModel({"email": self.__email})
        if user:
            isgoodpwd = verify_password(self.__password, user["password"])
            if isgoodpwd:
                user["password"] = ""
                return user
            return None
        else:
            return None
    
    def update_password(self, id:str, old_password:str, new_password:str):
        user = self.get_by_id(id)
        isgoodpwd = verify_password(old_password, user["password"])
        if isgoodpwd:
            passw = self.validate_password(new_password)
            return self.updateModel({"_id":id}, {"password": hash_pwd(passw)})
        else:
            return None
    
    def updateTel(self, tel:str, code:str=""):
        if not code:
            # send code to number
            pass
        else:
            # check the code
            # if ok update tel
            return self.updateModel({"_id": self.getId()}, {"tel": tel})
    
    def updateProfil(self, profil:str):
        updt = {"profil": profil}
        if self.getId():
            return self.updateModel({"_id": self.getId()}, updt)
        else:
            return None
    
    def getProfil(self):
        return self.__profil
    
    def setProfil(self, profil:str):
        self.__profil = profil
    
    def validate_password(self, value:str):
        if len(value) < 8:
            raise HTTPException(status_code=400, detail={"error": "Password must be at least 8 characters long"})
        if not any(char.isdigit() for char in value):
            raise HTTPException(status_code=400, detail={"error": "Password must contain at least one digit"}) 
        if not any(char.isupper() for char in value):
            raise HTTPException(status_code=400, detail={"error": "Password must contain at least one uppercase letter"})  
        if not any(char.islower() for char in value):
            raise HTTPException(status_code=400, detail={"error": "Password must contain at least one lowercase letter"}) 
        if not any(char in "!@#$%^&*()_+-=" for char in value):
            raise HTTPException(status_code=400, detail={"error": "Password must contain at least one special character (!@#$%^&*()_+-=)"}) 
        return value
    
        