from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_valid_file():

    response = client.post("/upload", files={"file": ("test.jpg", b"fake image content", "image/jpeg")})
    assert response.status_code == 200
    assert response.json() == {
            "filename": "test.jpg", 
            "size": len(b"fake image content")
        }
    
def test_upload_invalid_extension():
    response = client.post("/upload", files={"file": ("test.exe", b"fake executable content", "application/octet-stream")})
    assert response.status_code == 400
    assert response.json() == {"detail": "File type not allowed"}

def test_upload_large_file():
    large_content = b"a" * (10 * 1024 * 1024 + 1)  # Just over 10MB
    response = client.post("/upload", files={"file": ("large.txt", large_content, "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"detail": "File size exceeds limit"}

def test_upload_no_file():
    response = client.post("/upload", files={})
    assert response.status_code == 422  # Unprocessable Entity due to missing file field