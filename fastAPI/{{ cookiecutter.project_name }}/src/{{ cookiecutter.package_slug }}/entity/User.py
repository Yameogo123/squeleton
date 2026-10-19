from datetime import UTC, datetime

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field

from {{ cookiecutter.package_slug }}.entity.Entity import Entity
from {{ cookiecutter.package_slug }}.utils.controller import blind_index, decrypt_text, encrypt_text, hash_pwd, verify_password

ENCRYPTED_FIELDS = ("nom", "prenom", "email", "adresse")
PRIVATE_FIELDS = ("password", "email_hash")
SPECIAL_CHARS = "!@#$%^&*()_+-=.,;:?"


class UserModel(BaseModel):
    """Sign-up payload. `role` is NOT accepted from clients (privilege escalation)."""

    nom: str = Field(min_length=1, max_length=100)
    prenom: str = Field(min_length=1, max_length=100)
    email: EmailStr
    tel: str = Field(default="", max_length=20)
    adresse: str = Field(default="", max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserUpdateModel(BaseModel):
    nom: str | None = Field(default=None, min_length=1, max_length=100)
    prenom: str | None = Field(default=None, min_length=1, max_length=100)
    adresse: str | None = Field(default=None, max_length=255)


class LoginEmailModel(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class LoginTelModel(BaseModel):
    tel: str = Field(max_length=20)
    password: str = Field(max_length=128)


class UserPwdModel(BaseModel):
    oldPassword: str = Field(max_length=128)
    password: str = Field(min_length=8, max_length=128)


def _today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


class User(Entity):
    def __init__(self):
        super().__init__("user")

    @staticmethod
    def public(user: dict | None) -> dict | None:
        """Decrypted user without secrets: the only shape that may leave the API."""
        if not user:
            return None
        user = {k: v for k, v in user.items() if k not in PRIVATE_FIELDS}
        for field in ENCRYPTED_FIELDS:
            if field in user:
                user[field] = decrypt_text(user[field])
        return user

    async def create(self, data: UserModel) -> str | None:
        """Returns the new id, or None when the email/tel is already used."""
        self.validate_password(data.password)
        email_hash = blind_index(data.email)
        if await self.getModel({"email_hash": email_hash}):
            return None
        if data.tel and await self.getModel({"tel": data.tel}):
            return None
        document = data.model_dump()
        for field in ENCRYPTED_FIELDS:
            document[field] = encrypt_text(document[field])
        document.update(
            email_hash=email_hash,
            password=hash_pwd(data.password),
            role="user",
            actif=True,
            created_at=_today(),
        )
        return await self.saveModel(document)

    async def update(self, data: UserUpdateModel) -> int:
        changes = {k: encrypt_text(v) for k, v in data.model_dump(exclude_none=True).items()}
        if not self.getId() or not changes:
            return 0
        return await self.updateModel({"_id": self.getId()}, changes)

    async def delete(self) -> int:
        if self.getId():
            return await self.deleteModel({"_id": self.getId()})
        return 0

    async def getById(self, id) -> dict | None:
        return self.public(await self.getModel({"_id": id}))

    async def getAll(self, limit: int = 50, skip: int = 0) -> list[dict]:
        return [self.public(x) for x in await self.getModels(limit=limit, skip=skip)]

    async def _login(self, user: dict | None, password: str) -> dict | None:
        # verify_password runs even when the user doesn't exist (same response time)
        if not verify_password(password, user["password"] if user else None):
            return None
        if not user.get("actif", True):
            raise HTTPException(403, "Account disabled")
        return self.public(user)

    async def loginEmail(self, data: LoginEmailModel) -> dict | None:
        return await self._login(await self.getModel({"email_hash": blind_index(data.email)}), data.password)

    async def loginTel(self, data: LoginTelModel) -> dict | None:
        return await self._login(await self.getModel({"tel": data.tel}), data.password)

    async def updatePassword(self, id: str, old_password: str, new_password: str) -> int | None:
        user = await self.getModel({"_id": id})
        if not user or not verify_password(old_password, user["password"]):
            return None
        self.validate_password(new_password)
        return await self.updateModel({"_id": id}, {"password": hash_pwd(new_password), "last_pwd_update": _today()})

    async def updateTel(self, tel: str) -> int:
        if not self.getId():
            return 0
        return await self.updateModel({"_id": self.getId()}, {"tel": tel, "last_tel_update": _today()})

    async def updateField(self, field: str, value: str) -> int:
        """profil / cni / expo_token ..."""
        if not self.getId():
            return 0
        return await self.updateModel({"_id": self.getId()}, {field: value})

    @staticmethod
    def validate_password(value: str) -> str:
        rules = [
            (len(value) >= 8, "Password must be at least 8 characters long"),
            (any(c.isdigit() for c in value), "Password must contain at least one digit"),
            (any(c.isupper() for c in value), "Password must contain at least one uppercase letter"),
            (any(c.islower() for c in value), "Password must contain at least one lowercase letter"),
            (any(c in SPECIAL_CHARS for c in value), f"Password must contain a special character ({SPECIAL_CHARS})"),
        ]
        for ok, message in rules:
            if not ok:
                raise HTTPException(status_code=400, detail={"error": message})
        return value
