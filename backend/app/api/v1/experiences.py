from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.experience import Experience, ExperienceCreate, ExperienceUpdate, ExperienceList
from app.services.experience_service import experience_service

router = APIRouter()


@router.get("/", response_model=List[Experience])
async def get_experiences(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    company: Optional[str] = None,
    position: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取经验列表"""
    experiences = experience_service.get_experiences(
        db, skip=skip, limit=limit, company=company, position=position
    )
    return experiences


@router.get("/{experience_id}", response_model=Experience)
async def get_experience(experience_id: int, db: Session = Depends(get_db)):
    """获取单个经验"""
    experience = experience_service.get_experience(db, experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )
    return experience


@router.post("/", response_model=Experience)
async def create_experience(
    experience: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建经验"""
    db_experience = experience_service.create_experience(
        db, experience, current_user.phone
    )
    return db_experience


@router.put("/{experience_id}", response_model=Experience)
async def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新经验"""
    db_experience = experience_service.update_experience(
        db, experience_id, experience_update, current_user.phone
    )
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found or not authorized"
        )
    return db_experience


@router.delete("/{experience_id}")
async def delete_experience(
    experience_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除经验"""
    success = experience_service.delete_experience(
        db, experience_id, current_user.phone
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found or not authorized"
        )
    return {"message": "Experience deleted successfully"}


@router.get("/search/", response_model=List[Experience])
async def search_experiences(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索经验"""
    experiences = experience_service.search_experiences(db, q, skip, limit)
    return experiences 