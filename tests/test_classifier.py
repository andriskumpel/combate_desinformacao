import pytest
from app.services.classifier import ContentClassifier
from app.core.config import settings

@pytest.fixture
def classifier():
    return ContentClassifier()

@pytest.mark.asyncio
async def test_text_classification(classifier):
    # Test text classification
    analysis = {
        "type": "text",
        "content": "A vacina contra COVID-19 é segura e eficaz.",
        "sentiment": [{"label": "positive", "score": 0.9}],
        "entities": [],
        "topics": ["saúde", "vacina"],
        "metadata": {"length": 40, "language": "pt"}
    }
    
    result = await classifier.classify(analysis)
    
    assert "label" in result
    assert "confidence" in result
    assert "explanation" in result
    assert "sources" in result
    assert result["label"] in settings.CLASSIFICATION_LABELS.values()

@pytest.mark.asyncio
async def test_image_classification(classifier):
    # Test image classification
    analysis = {
        "type": "image",
        "classification": [{"label": "medical", "score": 0.8}],
        "metadata": {
            "format": "JPEG",
            "size": (800, 600),
            "mode": "RGB"
        }
    }
    
    result = await classifier.classify(analysis)
    
    assert "label" in result
    assert "confidence" in result
    assert "explanation" in result
    assert "sources" in result
    assert result["label"] in settings.CLASSIFICATION_LABELS.values()

@pytest.mark.asyncio
async def test_video_classification(classifier):
    # Test video classification
    analysis = {
        "type": "video",
        "metadata": {
            "fps": 30,
            "frame_count": 300,
            "width": 1920,
            "height": 1080
        },
        "analysis": {
            "key_frames": [],
            "objects": [],
            "scenes": []
        }
    }
    
    result = await classifier.classify(analysis)
    
    assert "label" in result
    assert "confidence" in result
    assert "explanation" in result
    assert "sources" in result
    assert result["label"] in settings.CLASSIFICATION_LABELS.values()

@pytest.mark.asyncio
async def test_invalid_content_type(classifier):
    # Test invalid content type
    analysis = {
        "type": "invalid_type",
        "content": "test content"
    }
    
    with pytest.raises(ValueError):
        await classifier.classify(analysis) 