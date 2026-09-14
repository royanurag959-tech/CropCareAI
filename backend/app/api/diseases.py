from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Disease, Crop
from app.schemas.schemas import DiseaseResponse, CropResponse

router = APIRouter(prefix="/diseases", tags=["Disease Knowledgebase"])

@router.get("", response_model=List[DiseaseResponse])
def get_all_diseases(
    crop: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Disease).join(Crop)

    if crop:
        query = query.filter(Crop.name.ilike(f"%{crop}%"))
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Disease.name.ilike(search_fmt)) |
            (Disease.hindi_name.ilike(search_fmt)) |
            (Disease.symptoms.ilike(search_fmt)) |
            (Crop.name.ilike(search_fmt))
        )
    if severity:
        query = query.filter(Disease.severity_level.ilike(severity))

    diseases = query.all()
    return [d.to_dict() for d in diseases]

@router.get("/crops", response_model=List[CropResponse])
def get_all_crops(db: Session = Depends(get_db)):
    crops = db.query(Crop).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "hindi_name": c.hindi_name,
            "description": c.description,
            "icon": c.icon
        }
        for c in crops
    ]

@router.get("/{disease_id}", response_model=DiseaseResponse)
def get_disease_by_id(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease record not found")
    return disease.to_dict()
