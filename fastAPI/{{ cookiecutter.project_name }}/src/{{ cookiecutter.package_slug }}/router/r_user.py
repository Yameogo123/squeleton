


from fastapi import APIRouter, Depends, File, UploadFile
from {{ cookiecutter.package_slug }}.middleware.middleware import JWTBearer, signJWT
from {{ cookiecutter.package_slug }}.utils.controller import http_error
from {{ cookiecutter.package_slug }}.entity.User import User, UserModel, UserPwd2Model
from {{ cookiecutter.package_slug }}.entity.Files import Files
from bson.objectid import ObjectId
from loguru import logger

r_user = APIRouter()




@r_user.post("/login")
async def login(user_info:UserModel):
    try:
        model = User()
        model.load(user_info)
        db_user = model.login()
        if db_user is None:
            http_error("Mauvaises données apportées!", 400) 
        if not db_user["actif"]:
            http_error("votre compte est inactif!", 400) 
        rs = signJWT(db_user["email"])
        db_user["access_token"] = rs["access_token"]
        return db_user
    except Exception as e:
        http_error(e, 400) 
    
@r_user.post("/login/tel", tags=['user'])
async def login2(user_info:UserModel):
    try:
        model = User()
        model.load(user_info)
        db_user = model.login2()
        if db_user == -1 or db_user == -2:
            http_error("Mauvaises données saisies!", 400) 
        if not db_user["actif"]:
            http_error("votre compte est inactif!", 400) 
        rs = signJWT(db_user["tel"])
        db_user["access_token"] = rs["access_token"]
        return db_user
    except Exception as e:
        http_error(e, 400) 

@r_user.post("/signin")
async def sign_user_up(user:UserModel):
    try:
        model = User()
        model.load(user)
        res = model.save()
        inserted = res.inserted_id
        if inserted:
            return {"message": "utilisateur créé avec succès", "state": "success"}
        else:
            return {"message": "utilisateur non sauvegardé", "state": "warning"}
    except Exception as e:
        message = str(e)
        if "duplicate key" in message:
            message = "Ce compte existe déjà (soit le mail ou le numero de téléphone)"
        http_error(message, 400) 

@r_user.get("/{id}", dependencies=[Depends(JWTBearer())])
async def getVehicule(id: str):
    us = User()
    try:
        res = us.getModel({"_id": ObjectId(id)})
        return {"user": res}
    except Exception as e:
        http_error(e, 400) 


@r_user.get("/s/all", dependencies=[Depends(JWTBearer())])
async def getAllUsers():
    try:
        user = User()
        users = user.getAll()
        return {"users": users}
    except Exception as e:
        http_error(e, 400) 


@r_user.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateUser(id:str, dico: UserModel):
    try:
        user = User()
        user.load(dico)
        user.setId(ObjectId(id))
        res= user.update()
        if res.modified_count > 0:
            return {"message": "utilisateur mis à jour avec succès", "state": "success"}
        else:
            return {"message": "rien a changé", "state": "warning"}
    except Exception as e:
        http_error(e, 400) 
        
        

@r_user.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteUser(id:str):
    try:
        user = User()
        user.setId(ObjectId(id))
        resp = user.delete()
        if resp.deleted_count > 0:
            return {"message": "utilisateur supprimé avec succès.", "state": "success"}
        else:
            return {"message": "Compte non supprimé!", "state": "warning"}
    except Exception as e:
        http_error(e, 400) 


@r_user.put("/update/{typee}/{id}", dependencies=[Depends(JWTBearer())]) # profil, cni
async def updateImage(typee:str, id:str, file: UploadFile = File(...)):
    try:
        user = User()
        mod = user.getModel({'_id': ObjectId(id)})
        user.setId(ObjectId(mod["_id"]))
        files = Files()
        files.load(file)
        if typee not in ("profil", "cni"):
            http_error("typee saisi doit être profil ou cni", 500)
        if typee in mod.keys():
            files.setId(mod[typee])
            res = files.delete()
            if res is None:
                logger.warning("pas d'ancienne image associée. Donc étape de suppression sautée")
        f_id = await files.save()       
        if f_id:
            if typee == "profil":
                resp = user.updateProfil(str(f_id), str(id))
            elif typee == "cni":
                resp = user.updateCNI(str(f_id), str(id))
            if resp.modified_count > 0:
                return {"message": "image mise à jour avec succès", "state": "success"}
            else:
                return {"message": "rien a changé", "state": "warning"}
        else:
            http_error("nouvelle image non sauvegardée", 500)
    except Exception as e:
        http_error(e, 500)
        
        

@r_user.put("/expo/{user_id}/{token}", dependencies=[Depends(JWTBearer())])
async def updateUserExpo(user_id:str, token: str):
    try:
        user = User()
        tk = token if token != "null" else ""
        res= user.updateExpoToken(tk, user_id)
        if res.modified_count > 0:
            return {"message": "token mis à jour", "state": "success"}
        else:
            return {"message": "rien a changé", "state": "warning"}
    except Exception as e:
        http_error(e, 400) 
        

@r_user.put("/v2/password")
async def updateUserPwd2(dico: UserPwd2Model):
    try:
        user = User()
        res= user.updatePassword2(dico)
        if res == 0:
            return {"message": "utilisateur inconnu! re-voyer vos saisis.", "state": "warning"}
        if res == 1:
            return {"message": "nouveau mot de passe ne respecte pas les critères!", "state": "warning"}
        if res.modified_count > 0:
            return {"message": "mot de passe mis à jour", "state": "success"}
        else:
            return {"message": "vous n'avez rien changé", "state": "warning"}
    except Exception:
        return {"message": "Mauvais mot de passe", "state": "error"}