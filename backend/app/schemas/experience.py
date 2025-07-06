from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.schemas.user import User


class ExperienceBase(BaseModel):
    company: str = Field(..., max_length=100, description="公司名称")
    position: str = Field(..., max_length=100, description="职位")
    summary: str = Field(..., description="经验总结")
    content: str = Field(..., description="详细内容")
    difficulty: float = Field(0.0, ge=0.0, le=5.0, description="难度评分")
    tags: Optional[List[str]] = Field(None, description="标签列表")


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    summary: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[float] = Field(None, ge=0.0, le=5.0)
    tags: Optional[List[str]] = None


class ExperienceInDB(ExperienceBase):
    id: int
    user_id: int
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        import json
        if v is None:
            return []
        if isinstance(v, list):
            return v
        try:
            return json.loads(v)
        except Exception:
            return []
    
    class Config:
        from_attributes = True


class Experience(ExperienceInDB):
    user: Optional[User] = None  # 用户信息


class ExperienceList(BaseModel):
    experiences: List[Experience]
    total: int
    page: int
    size: int 