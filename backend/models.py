from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Section(BaseModel):
    subtitle: str
    text: List[str]
    tips: Optional[str] = None

class Chapter(BaseModel):
    title: str
    description: str
    content: List[Section]

class EbookContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    author: str
    pages: int
    chapters: List[Chapter]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DownloadTracking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_agent: str
    ip_address: str
    filename: str

class Statistics(BaseModel):
    students_helped: int = 15000
    success_rate: int = 85
    avg_time_to_results: int = 30
    total_downloads: int = 0

class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str
    content: str
    rating: int = Field(ge=1, le=5)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PDFGenerationRequest(BaseModel):
    user_agent: str
    ip_address: str

class PDFGenerationResponse(BaseModel):
    success: bool
    download_url: str
    filename: str
    token: str