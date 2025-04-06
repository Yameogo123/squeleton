from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId
from loguru import logger

from {{ cookiecutter.package_slug }}.utils.controller import http_error
from {{ cookiecutter.package_slug }}.entity.Role import Role, RoleModel
from {{ cookiecutter.package_slug }}.entity.User import User, UserModel
from {{ cookiecutter.package_slug }}.entity.Files import Files
from {{ cookiecutter.package_slug }}.entity.IAChat import IAChat, IAChatModel
from {{ cookiecutter.package_slug }}.middleware.middleware import signJWT, JWTBearer

from decouple import config

import pretty_errors  # noqa: F401

PORT = config("PORT")

# Create FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Uvicorn!"}


############## role

@app.get("/role/{id}")
async def getRole(id: str):
    role = Role()
    try:
        res = role.getOne(ObjectId(id))
        return {"role": res}
    except Exception as e:
        http_error(e, 400) 

@app.post("/role/new")
async def saveRole(sent:RoleModel):
    try:
        role = Role()
        role.load(sent)
        result = role.save()
        inserted = result.inserted_id
        if inserted:
            return {"message": "role saved with success"}
        else:
            return {"message": "role not saved"}
    except Exception as e:
        http_error(e, 400) 

@app.put("/role/{id}", dependencies=[Depends(JWTBearer())])
async def updateRole(id:str, dico: RoleModel):
    try:
        role = Role()
        role.load(dico)
        role.setId(ObjectId(id))
        res= role.update()
        if res.modified_count > 0:
            return {"message": "role updated successfully"}
        else:
            return {"message": "you changed nothing"}
    except Exception as e:
        http_error(e, 400) 

@app.get("/roles/all")
async def getAllRole():
    try:
        role = Role()
        roles = role.getAll()
        return {"roles": roles}
    except Exception as e:
        http_error(e, 400) 

@app.delete("/role/{id}")
async def deleteRole(id:str):
    try:
        role = Role()
        role.setId(ObjectId(id))
        resp = role.delete()
        if resp.deleted_count > 0:
            return {"message": "role deleted with success"}
        else:
            return {"message": "role not deleted (id inexistant?)"}
    except Exception as e:
        http_error(e, 400) 



########### user

@app.post("/login")
async def login(user_info:UserModel):
    try:
        model = User()
        model.load(user_info)
        db_user = model.login()
        if db_user is None:
            http_error("Bad credentials. check email and password!", 400) 
        rs = signJWT(db_user["email"])
        db_user["access_token"] = rs["access_token"]
        return db_user
    except Exception as e:
        http_error(e, 400) 

@app.post("/signin")
async def sign_user_up(user:UserModel):
    try:
        model = User()
        model.load(user)
        res = model.save()
        inserted = res.inserted_id
        if inserted:
            return {"message": "user saved with success"}
        else:
            return {"message": "user not saved"}
    except Exception as e:
        http_error(e, 400) 

@app.get("/users/all")
async def getAllUsers():
    try:
        user = User()
        users = user.getAll()
        return {"users": users}
    except Exception as e:
        http_error(e, 400) 


@app.put("/user/{id}")
async def updateUser(id:str, dico: UserModel):
    try:
        user = User()
        user.load(dico)
        user.setId(ObjectId(id))
        res= user.update()
        if res.modified_count > 0:
            return {"message": "user updated successfully"}
        else:
            return {"message": "you changed nothing"}
    except Exception as e:
        http_error(e, 400) 


@app.delete("/user/{id}")
async def deleteUser(id:str):
    try:
        user = User()
        user.setId(ObjectId(id))
        resp = user.delete()
        if resp.deleted_count > 0:
            return {"message": "user deleted with success"}
        else:
            return {"message": "user not deleted (id inexistant?)"}
    except Exception as e:
        http_error(e, 400) 


@app.put("/set/profile/{id}")
async def setProfile(id:str, file: UploadFile = File(...)):
    try:
        user = User()
        mod = user.get_by_id(ObjectId(id))
        user.setId(ObjectId(mod["_id"]))
        files = Files()
        files.load(file)
        if "profil" in mod.keys():
            files.setId(mod["profil"])
            res = files.delete()
            if res is None:
                logger.warning("user profil not deleted")
        f_id = await files.save()       
        if f_id:
            resp = user.updateProfil(str(f_id))
            if resp.modified_count > 0:
                return {"message": "user profile updated successfully"}
            else:
                return {"message": "you changed nothing"}
        else:
            http_error("new file not saved", 500)
    except Exception as e:
        http_error(e, 500) 


########## file

@app.get("/image/{file_id}")
async def get_image(file_id: str):
    try:
        file = Files()
        file.setId(ObjectId(file_id))
        return file.getStreaming()
    except Exception as e:
        http_error(e, 500) 

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    try:
        file = Files()
        file.setId(ObjectId(file_id))
        return file.download()
    except Exception as e:
        http_error(e, 500) 



######## IA chat
@app.post("/ia/medecin/send")
async def chatMedecin(chat: IAChatModel):
    try:
        iaChat = IAChat()
        iaChat.load(chat)
        result = iaChat.respond()
        return {"response": result}
    except Exception as e:
        http_error(e, 500)


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",  # Points to the "app" instance in the "main" module
#         host="0.0.0.0",  # Accessible on your network
#         port= int(PORT),       # Port to listen on
#         reload=True      # Enable auto-reload for development
#     )
    

