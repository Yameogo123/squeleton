from fastapi import HTTPException, UploadFile
from fastapi.responses import Response

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.entity.Entity import Entity

# Magic bytes of the allowed types: the client-provided content-type alone can't be trusted
_SIGNATURES = {
    "image/png": [b"\x89PNG\r\n\x1a\n"],
    "image/jpeg": [b"\xff\xd8\xff"],
    "image/webp": [b"RIFF"],
    "application/pdf": [b"%PDF-"],
}


class Files(Entity):
    def __init__(self, file: UploadFile | None = None):
        super().__init__("files")
        self.__file = file

    def load(self, file: UploadFile):
        self.__file = file

    async def _validated_content(self) -> bytes:
        file = self.__file
        if file.content_type not in settings.ALLOWED_UPLOAD_TYPES:
            raise HTTPException(415, f"File type not allowed: {file.content_type}")
        content = await file.read(settings.MAX_UPLOAD_SIZE + 1)
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(413, "File too large")
        signatures = _SIGNATURES.get(file.content_type)
        if signatures and not any(content.startswith(sig) for sig in signatures):
            raise HTTPException(415, "File content does not match its type")
        return content

    async def save(self) -> str | None:
        if not self.__file:
            return None
        content = await self._validated_content()
        return await self.newFile(self.__file.filename or "file", content, self.__file.content_type)

    async def delete(self):
        if self.getId():
            return await self.deleteFile(self.getId())
        return None

    async def _response(self, disposition: str) -> Response | None:
        if not self.getId():
            return None
        found = await self.getFileById(self.getId())
        if not found:
            return None
        content, filename, content_type = found
        safe_name = "".join(c for c in filename if c.isalnum() or c in "._-") or "file"
        return Response(
            content,
            media_type=content_type,
            headers={
                "Content-Disposition": f'{disposition}; filename="{safe_name}"',
                # files are immutable (new upload = new id): let browsers/CDN cache them
                "Cache-Control": "private, max-age=86400, immutable",
            },
        )

    async def getStreaming(self):
        return await self._response("inline")

    async def download(self):
        return await self._response("attachment")

    async def deleteGroup(self, ids: list[str]):
        return [await self.deleteFile(_id) for _id in ids]
