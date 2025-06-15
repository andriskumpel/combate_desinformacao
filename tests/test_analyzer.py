import pytest
import os
from app.services.analyzer import ContentAnalyzer

@pytest.fixture
def analyzer():
    return ContentAnalyzer()

@pytest.fixture
def test_image():
    # Create a simple test image
    from PIL import Image
    import io
    
    # Create a 100x100 RGB image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

@pytest.fixture
def test_video():
    # Create a simple test video
    import cv2
    import numpy as np
    import io
    
    # Create a 1-second video with 30 fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp.mp4', fourcc, 30.0, (640,480))
    
    for _ in range(30):  # 30 frames = 1 second
        frame = np.zeros((480,640,3), np.uint8)
        frame[:] = (0,0,255)  # Red frame
        out.write(frame)
    
    out.release()
    
    # Read the video file into bytes
    with open('temp.mp4', 'rb') as f:
        video_data = f.read()
    
    # Clean up
    os.remove('temp.mp4')
    return video_data

@pytest.mark.asyncio
async def test_text_analysis(analyzer):
    # Test text analysis
    text = "A vacina contra COVID-19 é segura e eficaz."
    result = await analyzer.analyze(text, "text")
    
    assert result["type"] == "text"
    assert "sentiment" in result
    assert "entities" in result
    assert "topics" in result
    assert "metadata" in result

@pytest.mark.asyncio
async def test_image_analysis(analyzer, test_image):
    # Test image analysis with a real test image
    result = await analyzer.analyze(test_image, "image")
    
    assert result["type"] == "image"
    assert "classification" in result
    assert "metadata" in result
    assert result["metadata"]["format"] == "JPEG"
    assert result["metadata"]["size"] == (100, 100)
    assert result["metadata"]["mode"] == "RGB"

@pytest.mark.asyncio
async def test_video_analysis(analyzer, test_video):
    # Test video analysis with a real test video
    result = await analyzer.analyze(test_video, "video")
    
    assert result["type"] == "video"
    assert "metadata" in result
    assert "analysis" in result
    assert "key_frames" in result["analysis"]
    assert "objects" in result["analysis"]
    assert "scenes" in result["analysis"]
    assert result["metadata"]["fps"] == 30.0
    assert result["metadata"]["width"] == 640
    assert result["metadata"]["height"] == 480

@pytest.mark.asyncio
async def test_invalid_content_type(analyzer):
    # Test invalid content type
    with pytest.raises(ValueError):
        await analyzer.analyze("test content", "invalid_type") 