"""
Asset model for tracking user devices and software.

This module defines the SQLAlchemy ORM model for assets and the Pydantic
schemas for asset-related API operations (create, update, list, etc).

- The `Asset` class is the database model for assets.
- The `AssetType` enum defines the type of asset (hardware, software, etc).
- The Pydantic models (`AssetBase`, `AssetCreate`, `AssetUpdate`, `AssetResponse`, `AssetListResponse`) are used for request/response validation and serialization.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.db import Base
from pydantic import BaseModel, Field  # Ensure compatibility with Pydantic v2
from typing import Optional, List
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    """Asset type enumeration."""
    HARDWARE = "hardware"
    SOFTWARE = "software"
    FIRMWARE = "firmware"
    OPERATING_SYSTEM = "operating_system"


class Asset(Base):
    """SQLAlchemy Asset model."""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)  # hardware, software, firmware, etc.
    vendor = Column(String, nullable=True)
    product = Column(String, nullable=True)
    version = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    cpe_string = Column(String, nullable=True)  # Common Platform Enumeration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="assets")
    alerts = relationship("Alert", back_populates="asset")


# Pydantic models for API
class AssetBase(BaseModel):
    """Base asset schema."""
    name: str
    asset_type: AssetType
    vendor: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    cpe_string: Optional[str] = None
    
    model_config = {"from_attributes": True}


class AssetCreate(AssetBase):
    """Schema for asset creation."""
    pass
    
    model_config = {"from_attributes": True}


class AssetUpdate(BaseModel):
    """Schema for asset updates."""
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    vendor: Optional[str] = None
    product: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    cpe_string: Optional[str] = None
    
    model_config = {"from_attributes": True}


class AssetResponse(AssetBase):
    """Schema for asset response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class AssetListResponse(BaseModel):
    """Schema for asset list response."""
    assets: List[AssetResponse]
    total: int
    page: int
    size: int
    
    model_config = {"from_attributes": True}