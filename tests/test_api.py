import pytest
from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

@pytest.fixture
def test_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs_url" in data

def test_verify_text_endpoint():
    # Test text verification
    payload = {
        "content": "A vacina contra COVID-19 é segura e eficaz.",
        "content_type": "text",
        "source_url": "https://example.com/article"
    }
    
    response = client.post("/api/v1/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "verification_id" in data
    assert "status" in data
    assert "confidence" in data
    assert "classification" in data
    assert "explanation" in data
    assert "sources" in data

def test_verify_file_endpoint(test_image):
    # Test file verification with a real test image
    files = {
        "file": ("test_image.jpg", test_image, "image/jpeg")
    }
    data = {
        "content_type": "image",
        "source_url": "https://example.com/image"
    }
    
    response = client.post("/api/v1/verify/file", files=files, data=data)
    assert response.status_code == 200
    data = response.json()
    
    assert "verification_id" in data
    assert "status" in data
    assert "confidence" in data
    assert "classification" in data
    assert "explanation" in data
    assert "sources" in data

def test_verification_status_endpoint():
    # First create a verification
    payload = {
        "content": "Test content",
        "content_type": "text"
    }
    create_response = client.post("/api/v1/verify", json=payload)
    verification_id = create_response.json()["verification_id"]
    
    # Then check its status
    response = client.get(f"/api/v1/status/{verification_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "message" in data

def test_invalid_content_type():
    # Test with invalid content type
    payload = {
        "content": "Test content",
        "content_type": "invalid_type"
    }
    
    response = client.post("/api/v1/verify", json=payload)
    assert response.status_code == 500

def test_missing_required_fields():
    # Test with missing required fields
    payload = {
        "content": "Test content"
        # Missing content_type
    }
    
    response = client.post("/api/v1/verify", json=payload)
    assert response.status_code == 422  # Validation error 