import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, storage_path: str = "/tmp/pdfs/"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles for PDF generation"""
        self.styles = getSampleStyleSheet()
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#4F46E5'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=HexColor('#6B7280'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Chapter title style
        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#4F46E5'),
            spaceBefore=30,
            spaceAfter=15
        ))
        
        # Section title style
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#1F2937'),
            spaceBefore=20,
            spaceAfter=10
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor('#374151'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Tips style
        self.styles.add(ParagraphStyle(
            name='TipsStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#1E40AF'),
            alignment=TA_LEFT,
            spaceAfter=15,
            leftIndent=20,
            rightIndent=20,
            backColor=HexColor('#EBF4FF'),
            borderColor=HexColor('#3B82F6'),
            borderWidth=1,
            borderPadding=10
        ))
    
    def generate_pdf(self, ebook_content: Dict[str, Any]) -> str:
        """Generate PDF from ebook content"""
        try:
            # Generate unique filename
            token = str(uuid.uuid4())
            filename = f"ebook_{token}.pdf"
            filepath = self.storage_path / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build PDF content
            story = []
            
            # Title page
            self._add_title_page(story, ebook_content)
            story.append(PageBreak())
            
            # Table of contents
            self._add_table_of_contents(story, ebook_content)
            story.append(PageBreak())
            
            # Chapters
            for i, chapter in enumerate(ebook_content['chapters']):
                self._add_chapter(story, chapter, i + 1)
                if i < len(ebook_content['chapters']) - 1:
                    story.append(PageBreak())
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF generated successfully: {filename}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    def _add_title_page(self, story: list, ebook_content: Dict[str, Any]):
        """Add title page to PDF"""
        story.append(Spacer(1, 2*inch))
        
        # Title
        story.append(Paragraph(ebook_content['title'], self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        story.append(Paragraph(ebook_content['subtitle'], self.styles['CustomSubtitle']))
        story.append(Spacer(1, 1*inch))
        
        # Author
        story.append(Paragraph(f"Par {ebook_content['author']}", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Date
        story.append(Paragraph(f"© {datetime.now().year}", self.styles['CustomSubtitle']))
    
    def _add_table_of_contents(self, story: list, ebook_content: Dict[str, Any]):
        """Add table of contents to PDF"""
        story.append(Paragraph("Table des Matières", self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        for i, chapter in enumerate(ebook_content['chapters']):
            toc_entry = f"Chapitre {i + 1}: {chapter['title']}"
            story.append(Paragraph(toc_entry, self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
    
    def _add_chapter(self, story: list, chapter: Dict[str, Any], chapter_num: int):
        """Add a chapter to PDF"""
        # Chapter title
        chapter_title = f"Chapitre {chapter_num}: {chapter['title']}"
        story.append(Paragraph(chapter_title, self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Chapter description
        if chapter.get('description'):
            story.append(Paragraph(chapter['description'], self.styles['CustomSubtitle']))
            story.append(Spacer(1, 0.3*inch))
        
        # Chapter content
        for section in chapter['content']:
            # Section title
            story.append(Paragraph(section['subtitle'], self.styles['SectionTitle']))
            story.append(Spacer(1, 0.1*inch))
            
            # Section text
            for paragraph in section['text']:
                story.append(Paragraph(paragraph, self.styles['CustomBody']))
                story.append(Spacer(1, 0.1*inch))
            
            # Tips if available
            if section.get('tips'):
                tip_text = f"💡 <b>Conseil Pro :</b> {section['tips']}"
                story.append(Paragraph(tip_text, self.styles['TipsStyle']))
            
            story.append(Spacer(1, 0.2*inch))
    
    def get_pdf_path(self, token: str) -> Path:
        """Get PDF file path from token"""
        filename = f"ebook_{token}.pdf"
        return self.storage_path / filename
    
    def cleanup_old_pdfs(self, hours: int = 24):
        """Clean up PDFs older than specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            for pdf_file in self.storage_path.glob("ebook_*.pdf"):
                if pdf_file.stat().st_mtime < cutoff_time.timestamp():
                    pdf_file.unlink()
                    logger.info(f"Cleaned up old PDF: {pdf_file.name}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old PDFs: {str(e)}")
    
    def pdf_exists(self, token: str) -> bool:
        """Check if PDF exists for given token"""
        return self.get_pdf_path(token).exists()