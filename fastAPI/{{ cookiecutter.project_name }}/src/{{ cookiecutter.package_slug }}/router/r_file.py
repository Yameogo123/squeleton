
from fastapi import APIRouter, File, UploadFile, Depends
from {{ cookiecutter.package_slug }}.middleware.middleware import JWTBearer
from {{ cookiecutter.package_slug }}.utils.controller import http_error
from {{ cookiecutter.package_slug }}.entity.Files import Files
from bson.objectid import ObjectId

r_file = APIRouter()

@r_file.get("/image/{file_id}")
async def get_image(file_id: str):
    try:
        file = Files()
        file.setId(ObjectId(file_id))
        return file.getStreaming()
    except Exception as e:
        http_error(e, 500) 

@r_file.get("/download/{file_id}")
async def download_file(file_id: str):
    try:
        file = Files()
        file.setId(ObjectId(file_id))
        return file.download()
    except Exception as e:
        http_error(e, 500) 
        
@r_file.post("/file/save", dependencies=[Depends(JWTBearer())])
async def save_file(file: UploadFile = File(...)):
    try:
        files = Files()
        files.load(file)
        f_id = await files.save()
        if f_id:
            return {'result': f_id}
        else:
            return {'result': -1}
    except Exception as e:
        http_error(f"soucis de suvagarde de l'image: {e}", 500)

@r_file.delete("/file/{id}", dependencies=[Depends(JWTBearer())], tags=['file'])
async def deleteFile(id:str):
    try:
        files = Files()
        files.setId(ObjectId(id))
        resp = await files.delete()
        if resp.deleted_count > 0:
            return {"message": "file deleted with success"}
        else:
            return {"message": "file not deleted (id inexistant?)"}
    except Exception as e:
        http_error(e, 500)