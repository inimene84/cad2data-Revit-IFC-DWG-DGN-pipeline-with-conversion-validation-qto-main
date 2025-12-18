from typing import List, Dict, Any
import logging
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)

def process_pdf_page(page, page_num: int, material_keywords: List[str]) -> Dict:
    """Process a single PDF page"""
    try:
        text = page.get_text()
        
        # If minimal text, try OCR
        if len(text.strip()) < 50:
            try:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img, lang='eng+est')  # Added Estonian
            except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError) as e:
                logger.warning(f"OCR failed on page {page_num + 1}: {e}")
                return {"page": page_num + 1, "text": "", "construction_items": []}

        # Process lines for construction data
        lines = text.split('\n')
        page_data = []
        construction_items = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 5:
                # Check for material keywords
                line_lower = line.lower()
                for keyword in material_keywords:
                    if keyword in line_lower:
                        # Try to extract quantity
                        import re
                        numbers = re.findall(r'\d+(?:\.\d+)?', line)
                        quantity = float(numbers[0]) if numbers else None

                        construction_items.append({
                            'material': keyword,
                            'text': line,
                            'page': page_num + 1,
                            'quantity': quantity,
                            'unit': 'unit'  # Default unit
                        })
                        break

                page_data.append({
                    'page': page_num + 1,
                    'text': line
                })

        return {
            "page": page_num + 1,
            "text": page_data,
            "construction_items": construction_items
        }
    except Exception as e:
        logger.error(f"Error processing page {page_num + 1}: {e}")
        return {"page": page_num + 1, "text": [], "construction_items": []}
