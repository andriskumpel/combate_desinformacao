from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel
from app.services.analyzer import ContentAnalyzer
from app.services.classifier import ContentClassifier
from app.core.config import settings
from app.repositories.verification import VerificationRepository
from app.models.database import VerificationCreate, VerificationInDB

router = APIRouter()
verification_repository = VerificationRepository()

class VerificationRequest(BaseModel):
    content: str
    content_type: str  # "text", "image", or "video"
    source_url: Optional[str] = None

class VerificationResponse(BaseModel):
    verification_id: str
    status: str
    confidence: float
    classification: str
    explanation: str
    sources: List[str]

@router.post("/verify", response_model=VerificationResponse)
async def verify_content(request: VerificationRequest):
    try:
        # Create verification record
        verification = VerificationCreate(
            content=request.content,
            content_type=request.content_type,
            source_url=request.source_url
        )
        verification_db = await verification_repository.create(verification)
        
        # Initialize analyzer and classifier
        analyzer = ContentAnalyzer()
        classifier = ContentClassifier()
        
        # Analyze content
        analysis_result = await analyzer.analyze(
            content=request.content,
            content_type=request.content_type
        )
        
        # Classify content
        classification_result = await classifier.classify(analysis_result)
        
        # Update verification record with results
        await verification_repository.update(
            verification_db.id,
            VerificationUpdate(
                analysis_result=analysis_result,
                classification_result=classification_result,
                status="completed"
            )
        )
        
        return VerificationResponse(
            verification_id=str(verification_db.id),
            status="completed",
            confidence=classification_result["confidence"],
            classification=classification_result["label"],
            explanation=classification_result["explanation"],
            sources=classification_result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify/file", response_model=VerificationResponse)
async def verify_file(
    file: UploadFile = File(...),
    content_type: str = Form(...),
    source_url: Optional[str] = Form(None)
):
    try:
        # Validate content type
        if content_type not in ["image", "video"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid content type: {content_type}. Must be 'image' or 'video'"
            )
        
        # Validate file extension
        file_ext = file.filename.split('.')[-1].lower()
        if content_type == "image" and file_ext not in ["jpg", "jpeg", "png", "gif"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image format: {file_ext}. Supported formats: jpg, jpeg, png, gif"
            )
        elif content_type == "video" and file_ext not in ["mp4", "avi", "mov"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid video format: {file_ext}. Supported formats: mp4, avi, mov"
            )
        
        # Read file content
        content = await file.read()
        
        # Create verification record
        verification = VerificationCreate(
            content=str(content),  # Convert bytes to string for storage
            content_type=content_type,
            source_url=source_url
        )
        verification_db = await verification_repository.create(verification)
        
        # Initialize analyzer and classifier
        analyzer = ContentAnalyzer()
        classifier = ContentClassifier()
        
        # Analyze content
        analysis_result = await analyzer.analyze(
            content=content,
            content_type=content_type
        )
        
        # Classify content
        classification_result = await classifier.classify(analysis_result)
        
        # Update verification record with results
        await verification_repository.update(
            verification_db.id,
            VerificationUpdate(
                analysis_result=analysis_result,
                classification_result=classification_result,
                status="completed"
            )
        )
        
        return VerificationResponse(
            verification_id=str(verification_db.id),
            status="completed",
            confidence=classification_result["confidence"],
            classification=classification_result["label"],
            explanation=classification_result["explanation"],
            sources=classification_result["sources"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{verification_id}")
async def get_verification_status(verification_id: str):
    verification = await verification_repository.get_by_id(verification_id)
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    return {
        "status": verification.status,
        "analysis_result": verification.analysis_result,
        "classification_result": verification.classification_result
    } 