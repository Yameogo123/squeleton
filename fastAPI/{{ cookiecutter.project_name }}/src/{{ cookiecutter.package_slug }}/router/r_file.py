from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from {{ cookiecutter.package_slug }}.entity.Files import Files
from {{ cookiecutter.package_slug }}.middleware.middleware import get_current_user
from {{ cookiecutter.package_slug }}.utils.limiter import limiter

r_file = APIRouter()

# File responses are not put in fastapi-cache (binary payloads); they send
# Cache-Control headers instead so browsers / a CDN cache them.


async def _file_response(file_id: str, inline: bool):
    file = Files()
    file.setId(file_id)
    response = await (file.getStreaming() if inline else file.download())
    if response is None:
        raise HTTPException(404, "File not found")
    return response


@r_file.get("/image/{file_id}")
@limiter.limit("30/second")
async def get_image(request: Request, file_id: str):
    return await _file_response(file_id, inline=True)


@r_file.get("/download/{file_id}")
@limiter.limit("10/second")
async def download_file(request: Request, file_id: str, current: dict = Depends(get_current_user)):
    return await _file_response(file_id, inline=False)


@r_file.post("/file/save", status_code=201)
@limiter.limit("5/second")
async def save_file(request: Request, file: UploadFile = File(...), current: dict = Depends(get_current_user)):
    f_id = await Files(file).save()
    if not f_id:
        raise HTTPException(500, "File not saved")
    return {"result": f_id}


@r_file.delete("/file/{id}")
@limiter.limit("5/second")
async def delete_file(request: Request, id: str, current: dict = Depends(get_current_user)):
    file = Files()
    file.setId(id)
    if await file.delete():
        return {"message": "File deleted"}
    raise HTTPException(404, "File not found")
