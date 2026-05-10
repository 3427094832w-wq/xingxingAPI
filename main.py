from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uuid, os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "仅允许图片"})
    fname = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"url": f"/uploads/{fname}"}

@app.get("/")
def root():
    return {"msg": "API running"}
