# Billing Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/billing.py
# Basic billing and pricing endpoints

from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/billing", tags=["billing"])

# VAT rates by country
VAT_RATES = {
    "EE": 0.22,  # Estonia
    "FI": 0.24,  # Finland
    "DE": 0.19,  # Germany
    "LV": 0.21,  # Latvia
    "LT": 0.21,  # Lithuania
}


@router.get("/vat-rates")
async def get_vat_rates():
    """Get VAT rates for supported countries"""
    return {
        "rates": VAT_RATES,
        "default_rate": 0.22,
        "default_country": "EE",
        "last_updated": "2024-01-01"
    }


@router.post("/calculate-vat")
async def calculate_vat(amount: float, country: str = "EE"):
    """Calculate VAT for a given amount"""
    vat_rate = VAT_RATES.get(country.upper(), 0.22)
    vat_amount = amount * vat_rate
    total = amount + vat_amount
    
    return {
        "net_amount": round(amount, 2),
        "vat_rate": vat_rate,
        "vat_amount": round(vat_amount, 2),
        "total_amount": round(total, 2),
        "country": country.upper(),
        "currency": "EUR"
    }


@router.get("/pricing")
async def get_pricing():
    """Get service pricing information"""
    return {
        "currency": "EUR",
        "services": [
            {
                "name": "PDF Extraction",
                "price_per_file": 0.00,
                "description": "Extract construction data from PDF files"
            },
            {
                "name": "Excel Processing",
                "price_per_file": 0.00,
                "description": "Process Excel quantity takeoffs"
            },
            {
                "name": "Cost Estimation",
                "price_per_query": 0.00,
                "description": "Semantic search in DDC CWICR database"
            }
        ],
        "note": "Currently in development - all services are free"
    }
