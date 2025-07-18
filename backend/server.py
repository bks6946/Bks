from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import Dict, Any
from models import PDFGenerationRequest, PDFGenerationResponse, Statistics
from services import EbookService
from pdf_generator import PDFGenerator
import asyncio


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
pdf_generator = PDFGenerator()
ebook_service = EbookService(db, pdf_generator)

# Create the main app without a prefix
app = FastAPI(
    title="Ebook Student API",
    description="API pour la plateforme d'ebook étudiant",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Ebook Student API is running"}

@api_router.get("/ebook/content")
async def get_ebook_content():
    """Get ebook content"""
    try:
        content = await ebook_service.get_ebook_content()
        return {"success": True, "data": content}
    except Exception as e:
        logging.error(f"Error getting ebook content: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving ebook content")

@api_router.post("/generate-pdf", response_model=PDFGenerationResponse)
async def generate_pdf(request: Request):
    """Generate PDF and return download token"""
    try:
        # Get client info
        user_agent = request.headers.get('user-agent', 'Unknown')
        ip_address = request.client.host
        
        # Generate PDF
        token = await ebook_service.generate_pdf(user_agent, ip_address)
        
        response = PDFGenerationResponse(
            success=True,
            download_url=f"/api/download-pdf/{token}",
            filename="comment-faire-1000-euros-en-1-mois.pdf",
            token=token
        )
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating PDF")

@api_router.get("/download-pdf/{token}")
async def download_pdf(token: str):
    """Download PDF file"""
    try:
        # Check if PDF exists
        if not pdf_generator.pdf_exists(token):
            raise HTTPException(status_code=404, detail="PDF not found or expired")
        
        # Get PDF path
        pdf_path = pdf_generator.get_pdf_path(token)
        
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename="comment-faire-1000-euros-en-1-mois.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error downloading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error downloading PDF")

@api_router.get("/stats", response_model=Statistics)
async def get_statistics():
    """Get platform statistics"""
    try:
        stats = await ebook_service.get_statistics()
        return stats
    except Exception as e:
        logging.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")

@api_router.get("/testimonials")
async def get_testimonials():
    """Get testimonials"""
    try:
        testimonials = await ebook_service.get_testimonials()
        return {"success": True, "data": testimonials}
    except Exception as e:
        logging.error(f"Error getting testimonials: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving testimonials")

# Background task to clean up old PDFs
async def cleanup_old_pdfs():
    """Background task to clean up old PDFs"""
    while True:
        try:
            pdf_generator.cleanup_old_pdfs(hours=24)
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            logging.error(f"Error in cleanup task: {str(e)}")
            await asyncio.sleep(3600)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting Ebook Student API...")
    # Start cleanup task
    asyncio.create_task(cleanup_old_pdfs())

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()