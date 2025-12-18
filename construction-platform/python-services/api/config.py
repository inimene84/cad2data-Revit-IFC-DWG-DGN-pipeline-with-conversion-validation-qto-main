MATERIAL_KEYWORDS = [
    'concrete', 'steel', 'rebar', 'wood', 'lumber', 'brick', 
    'stone', 'glass', 'insulation', 'roofing', 'drywall',
    'flooring', 'paint', 'electrical', 'plumbing', 'hvac',
    'betoon', 'teras', 'raud', 'puit', 'tellis', 'kivi',
    'klaas', 'soojustus', 'katus', 'põrand', 'värv',
    'elekter', 'torustik', 'ventilatsioon'
]

REGIONAL_MULTIPLIERS = {
    "Tallinn": 1.10,
    "Tartu": 1.00,
    "Pärnu": 1.05,
    "Narva": 0.95,
    "Viljandi": 0.98
}

# VAT Configuration (Estonia)
import os

VAT_RATE = float(os.getenv("VAT_RATE", "0.24"))  # Default: Estonia 24%
VAT_COUNTRY = os.getenv("VAT_COUNTRY", "EE")
VAT_LABEL = f"VAT ({int(VAT_RATE * 100)}%)"

# QDRANT Configuration (DDC CWICR - OpenConstructionEstimate)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION_EN = os.getenv("QDRANT_COLLECTION_EN", "ddc_cwicr_en")
QDRANT_COLLECTION_DE = os.getenv("QDRANT_COLLECTION_DE", "ddc_cwicr_de")

# OpenAI Configuration (for embeddings)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

