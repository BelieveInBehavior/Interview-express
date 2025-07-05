from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate
from typing import List, Optional
import json


class ExperienceService:
    def get_experience(self, db: Session, experience_id: int) -> Optional[Experience]:
        """获取单个经验"""
        return db.query(Experience).filter(Experience.id == experience_id).first()
    
    def get_experiences(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 10,
        company: Optional[str] = None,
        position: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Experience]:
        """获取经验列表"""
        query = db.query(Experience)
        
        if company:
            query = query.filter(Experience.company.contains(company))
        if position:
            query = query.filter(Experience.position.contains(position))
        if tags:
            # 简单的标签匹配，实际项目中可能需要更复杂的搜索
            for tag in tags:
                query = query.filter(Experience.tags.contains(tag))
        
        return query.order_by(desc(Experience.created_at)).offset(skip).limit(limit).all()
    
    def create_experience(self, db: Session, experience: ExperienceCreate, user_phone: str) -> Experience:
        """创建经验"""
        experience_data = experience.dict()
        if experience_data.get("tags"):
            experience_data["tags"] = json.dumps(experience_data["tags"])
        
        db_experience = Experience(**experience_data, user_phone=user_phone)
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    def update_experience(
        self, 
        db: Session, 
        experience_id: int, 
        experience_update: ExperienceUpdate,
        user_phone: str
    ) -> Optional[Experience]:
        """更新经验"""
        db_experience = self.get_experience(db, experience_id)
        if not db_experience or db_experience.user_phone != user_phone:
            return None
        
        update_data = experience_update.dict(exclude_unset=True)
        if update_data.get("tags"):
            update_data["tags"] = json.dumps(update_data["tags"])
        
        for field, value in update_data.items():
            setattr(db_experience, field, value)
        
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    def delete_experience(self, db: Session, experience_id: int, user_phone: str) -> bool:
        """删除经验"""
        db_experience = self.get_experience(db, experience_id)
        if not db_experience or db_experience.user_phone != user_phone:
            return False
        
        db.delete(db_experience)
        db.commit()
        return True
    
    def search_experiences(
        self, 
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[Experience]:
        """搜索经验"""
        return db.query(Experience).filter(
            (Experience.company.contains(query)) |
            (Experience.position.contains(query)) |
            (Experience.summary.contains(query)) |
            (Experience.content.contains(query)) |
            (Experience.tags.contains(query))
        ).order_by(desc(Experience.created_at)).offset(skip).limit(limit).all()


experience_service = ExperienceService() 