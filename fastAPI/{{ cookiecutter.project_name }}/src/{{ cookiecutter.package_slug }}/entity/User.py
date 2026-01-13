
from fastapi import HTTPException
from pydantic import BaseModel
from {{ cookiecutter.package_slug }}.entity.Entity import Entity
from {{ cookiecutter.package_slug }}.utils.controller import hash_pwd, verify_password, encrypt_text, decrypt_text
from datetime import datetime
from bson.objectid import ObjectId
from loguru import logger

class UserModel(BaseModel):
    nom: str = ""
    prenom : str = ""
    email: str = ""
    tel: str = ""
    adresse: str = ""
    password: str = ""
    role: str = ""
    specialite_id: str = ""
    cabinet_id: str = ""
    profil: str = ""
    last_pwd_update: str = ""
    last_tel_update: str = ""
     

class UserPwdModel(BaseModel):
    password: str
    oldPassword: str    

class UserPwd2Model(BaseModel):
    nom: str
    prenom: str
    tel: str 
    password: str


class User(Entity):
    
    def __init__(self):
        super().__init__("user")
        self.__current = datetime.now().strftime("%Y-%m-%d")

    def __user_decrypt(self, user):
        try:
            user["nom"] = decrypt_text(user["nom"])
            user["prenom"] = decrypt_text(user["prenom"])
            user["email"] = decrypt_text(user["email"])
            user["adresse"] = decrypt_text(user["adresse"])
        except Exception as e:
            logger.error(f"erreur: {e}")
        return user
    
    def load(self, entite: UserModel):
        self.__entite = self.to_json(entite)
        self.__nom = encrypt_text(self.__entite["nom"])
        self.__prenom = encrypt_text(self.__entite["prenom"])
        self.__email = encrypt_text(self.__entite["email"])
        self.__password = self.__entite["password"]
    
    def save(self):
        if self.__entite:
            if self.validate_password(self.__entite["password"]):
                now = datetime.now()
                current = now.strftime("%Y-%m-%d")
                self.__entite["created_at"] = current
                self.__entite["password"] = hash_pwd(self.__entite["password"])
                self.__entite['nom'] = self.__nom
                self.__entite['prenom'] = self.__prenom
                self.__entite['email'] = self.__email
                return self.saveModel(self.__entite)
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
    
    def getById(self, id):
        return self.__user_decrypt(self.getModel({"_id": id}))
    
    def getAll(self):
        models = self.getModels()
        users = []
        for x in models:
            users.append(self.__user_decrypt(x))
        return users
    
    def __login(self, user):
        if user:
            isgoodpwd = verify_password(self.__password, user["password"])
            if isgoodpwd:
                if not user["active"]:
                    return None
                user["password"] = ""
                return user
            return None
        else:
            return None
    
    def loginEmail(self):
        user = self.getModel({"email": decrypt_text(self.__email)})
        return self.__login(user)
    
    def loginTel(self):
        user = self.getModel({"tel": decrypt_text(self.__tel)})
        return self.__login(user)
    
    def updatePassword(self, id:str, old_password:str, new_password:str):
        user = self.getById(id)
        isgoodpwd = verify_password(old_password, user["password"])
        if isgoodpwd:
            passw = self.validate_password(new_password)
            return self.updateModel({"_id":id}, {"password": hash_pwd(passw), "last_pwd_update": self.__current})
        else:
            return None
    
    def updatePassword2(self, info:UserPwd2Model):
        user = self.getModel({'nom': encrypt_text(info.nom), 'prenom': encrypt_text(info.prenom), "tel": encrypt_text(info.tel)})
        if not user:
            return 0
        else:
            try:
                passw = self.validate_password(info.password)
                return self.updateModel({"_id": ObjectId(user["_id"])}, {"password": hash_pwd(passw), "last_pwd_update": self.__current})
            except Exception:
                return 1
    
    def updateTel(self, id:str, tel:str):
        user = self.getModel(ObjectId(id))
        if user:
            return self.updateModel({"_id": self.getId()}, {"tel": encrypt_text(tel), "last_tel_update": self.__current})
        return None
    
    def updateProfil(self, profil:str):
        updt = {"profil": profil}
        if self.getId():
            return self.updateModel({"_id": self.getId()}, updt)
        else:
            return None
    
    def updateExpoToken(self, expoToken:str):
        if self.getId():
            return self.updateModel({"_id": self.getId()}, {"expo_token": expoToken})
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
    
        