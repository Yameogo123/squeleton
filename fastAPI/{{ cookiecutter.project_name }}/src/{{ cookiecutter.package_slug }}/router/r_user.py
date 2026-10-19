from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi_cache.decorator import cache

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.entity.Files import Files
from {{ cookiecutter.package_slug }}.entity.User import LoginEmailModel, LoginTelModel, User, UserModel, UserPwdModel, UserUpdateModel
from {{ cookiecutter.package_slug }}.middleware.middleware import ensure_owner_or_admin, get_current_user, require_admin, signJWT
from {{ cookiecutter.package_slug }}.utils.limiter import limiter

r_user = APIRouter()


def _with_token(user: dict) -> dict:
    return {**user, **signJWT(user["_id"], user.get("role", "user"))}


@r_user.post("/login")
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login(request: Request, user_info: LoginEmailModel):
    db_user = await User().loginEmail(user_info)
    if db_user is None:
        raise HTTPException(401, "Invalid credentials")
    return _with_token(db_user)


@r_user.post("/login/tel")
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login_tel(request: Request, user_info: LoginTelModel):
    db_user = await User().loginTel(user_info)
    if db_user is None:
        raise HTTPException(401, "Invalid credentials")
    return _with_token(db_user)


@r_user.post("/signin", status_code=201)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def sign_user_up(request: Request, user: UserModel):
    user_id = await User().create(user)
    if user_id is None:
        raise HTTPException(409, "Account already exists (email or phone number)")
    return {"message": "User created", "state": "success", "id": user_id}


@r_user.get("/me")
async def me(current: dict = Depends(get_current_user)):
    user = await User().getById(current["sub"])
    if user is None:
        raise HTTPException(404, "User not found")
    return {"user": user}


@r_user.get("/s/all")
@cache(expire=settings.CACHE_TTL, namespace="user")
async def get_all_users(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    current: dict = Depends(require_admin),
):
    return {"users": await User().getAll(limit=limit, skip=skip)}


@r_user.put("/password")
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def update_password(request: Request, dico: UserPwdModel, current: dict = Depends(get_current_user)):
    res = await User().updatePassword(current["sub"], dico.oldPassword, dico.password)
    if res is None:
        raise HTTPException(400, "Wrong password")
    return {"message": "Password updated", "state": "success"}


@r_user.get("/{id}")
@cache(expire=settings.CACHE_TTL, namespace="user")
async def get_user(request: Request, id: str, current: dict = Depends(get_current_user)):
    ensure_owner_or_admin(current, id)
    user = await User().getById(id)
    if user is None:
        raise HTTPException(404, "User not found")
    return {"user": user}


@r_user.put("/{id}")
async def update_user(request: Request, id: str, dico: UserUpdateModel, current: dict = Depends(get_current_user)):
    ensure_owner_or_admin(current, id)
    user = User()
    user.setId(id)
    if await user.update(dico):
        return {"message": "User updated", "state": "success"}
    return {"message": "Nothing changed", "state": "warning"}


@r_user.delete("/{id}")
async def delete_user(request: Request, id: str, current: dict = Depends(get_current_user)):
    ensure_owner_or_admin(current, id)
    user = User()
    user.setId(id)
    if await user.delete():
        return {"message": "User deleted", "state": "success"}
    raise HTTPException(404, "User not found")


@r_user.put("/update/{typee}/{id}")
async def update_image(
    request: Request,
    typee: Literal["profil", "cni"],
    id: str,
    file: UploadFile = File(...),
    current: dict = Depends(get_current_user),
):
    ensure_owner_or_admin(current, id)
    user = User()
    existing = await user.getModel({"_id": id})
    if existing is None:
        raise HTTPException(404, "User not found")
    user.setId(id)

    f_id = await Files(file).save()
    if not f_id:
        raise HTTPException(500, "File not saved")
    if existing.get(typee):  # remove the previous image only once the new one is stored
        old = Files()
        old.setId(existing[typee])
        await old.delete()
    await user.updateField(typee, f_id)
    return {"message": "Image updated", "state": "success", "id": f_id}


@r_user.put("/expo/{user_id}")
async def update_user_expo(
    request: Request, user_id: str, token: str = Query(max_length=255), current: dict = Depends(get_current_user)
):
    ensure_owner_or_admin(current, user_id)
    user = User()
    user.setId(user_id)
    await user.updateField("expo_token", "" if token == "null" else token)  # noqa: S105
    return {"message": "Token updated", "state": "success"}
