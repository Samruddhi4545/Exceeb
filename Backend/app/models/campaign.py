import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from app.db.session import Base


class CampaignStatus(str, enum.Enum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.PLANNING)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    client = relationship("User", foreign_keys=[client_id])
    tasks = relationship("Task", back_populates="campaign")
    members = relationship("CampaignMember", back_populates="campaign")


class CampaignMember(Base):
    __tablename__ = "campaign_members"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="members")
    employee = relationship("User")