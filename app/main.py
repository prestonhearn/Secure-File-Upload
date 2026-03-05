import logging
import os
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

#Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("secure-upload")

#Config
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".jpg", ".jpeg",".png"}

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

def sanitize_filename(filename: str) -> str:
    return Path(filename).name

def validate_extension(filename: str):
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

@app.get("/", response_class=HTMLResponse)
def upload_form():
    return """
    <html>
        <head>
            <title>Upload File</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-size: 1.5em;  /* slightly bigger text */
                    text-align: center;
                    margin: 20px;
                    font-family: Arial, sans-serif;
                }
                input[type="file"], input[type="submit"] {
                    font-size: 1em;
                    padding: 10px;
                    margin: 10px 0;
                    width: 90%;
                }
            </style>
        </head>
        <body>
            <h2>Upload a File</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input type="file" name="file" required/>
                <br/>
                <input type="submit" value="Upload"/>
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Upload attempt: {file.filename}")

        safe_filename = sanitize_filename(file.filename)

        validate_extension(safe_filename)

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds limit")
        
        file_path = UPLOAD_DIR / safe_filename

        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"File uploaded successfully: {file.filename} | Size: {len(contents)} bytes | Saved to: {file_path}")

        return {
            "filename": file.filename, 
            "size": len(contents)
        }
    
    except HTTPException as e:
        logger.warning(f"Rejected file upload: {file.filename} | Reason: {e.detail}")
        raise e
    
    except Exception as e:
        logger.exception("Unexpected error during file upload")
        raise HTTPException(status_code=500, detail="Internal Server Error")