# Billing Integration
# construction-platform/python-services/api/billing.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from decimal import Decimal
import os

# VAT Configuration
VAT_RATE = Decimal(os.getenv("VAT_RATE", "0.24"))  # Estonia 24%
VAT_COUNTRY = os.getenv("VAT_COUNTRY", "EE")

logger = logging.getLogger(__name__)

class BillingManager:
    """Billing manager for usage-based billing"""
    def __init__(self):
        self.pricing_plans: Dict[str, Dict[str, Any]] = {
            "free": {
                "name": "Free",
                "price": 0.0,
                "file_upload_limit": 100,
                "storage_limit_gb": 1,
                "api_calls_limit": 1000,
                "features": ["basic_processing", "basic_analytics"]
            },
            "starter": {
                "name": "Starter",
                "price": 29.0,
                "file_upload_limit": 1000,
                "storage_limit_gb": 10,
                "api_calls_limit": 10000,
                "features": ["basic_processing", "basic_analytics", "priority_support"]
            },
            "professional": {
                "name": "Professional",
                "price": 99.0,
                "file_upload_limit": 10000,
                "storage_limit_gb": 100,
                "api_calls_limit": 100000,
                "features": ["advanced_processing", "advanced_analytics", "priority_support", "custom_workflows"]
            },
            "enterprise": {
                "name": "Enterprise",
                "price": 299.0,
                "file_upload_limit": -1,  # Unlimited
                "storage_limit_gb": -1,  # Unlimited
                "api_calls_limit": -1,  # Unlimited
                "features": ["all_features", "custom_integrations", "dedicated_support", "sla"]
            }
        }
        
        self.usage_pricing: Dict[str, Decimal] = {
            "file_upload": Decimal("0.10"),  # $0.10 per file
            "storage_gb": Decimal("0.05"),  # $0.05 per GB per month
            "api_call": Decimal("0.001"),  # $0.001 per API call
            "processing_minute": Decimal("0.50"),  # $0.50 per processing minute
        }
    
    def get_pricing_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get pricing plan by ID"""
        return self.pricing_plans.get(plan_id)
    
    def calculate_usage_cost(self, tenant_id: str, usage_stats: Dict[str, Any]) -> Decimal:
        """Calculate usage-based cost"""
        try:
            total_cost = Decimal("0.0")
            
            # File upload cost
            files_uploaded = usage_stats.get("files_uploaded", 0)
            total_cost += Decimal(str(files_uploaded)) * self.usage_pricing["file_upload"]
            
            # Storage cost
            storage_gb = usage_stats.get("storage_used", 0) / (1024 ** 3)  # Convert to GB
            total_cost += Decimal(str(storage_gb)) * self.usage_pricing["storage_gb"]
            
            # API call cost
            api_calls = usage_stats.get("api_calls", 0)
            total_cost += Decimal(str(api_calls)) * self.usage_pricing["api_call"]
            
            # Processing cost (estimated)
            processing_minutes = usage_stats.get("processing_minutes", 0)
            total_cost += Decimal(str(processing_minutes)) * self.usage_pricing["processing_minute"]
            
            return total_cost
        except Exception as e:
            logger.error(f"Failed to calculate usage cost: {e}")
            return Decimal("0.0")
    
    def generate_invoice(self, tenant_id: str, period: str = "monthly") -> Dict[str, Any]:
        """Generate invoice for tenant"""
        try:
            # Get tenant plan
            tenant_plan = self.get_pricing_plan("professional")  # Default plan
            base_cost = Decimal(str(tenant_plan["price"]))
            
            # Get usage stats
            from usage_analytics import usage_tracker
            if usage_tracker:
                usage_stats = usage_tracker.get_usage_stats(tenant_id, period="30d")
                usage_cost = self.calculate_usage_cost(tenant_id, usage_stats)
            else:
                usage_cost = Decimal("0.0")
                usage_stats = {}
            
            # Calculate total (before VAT)
            subtotal = base_cost + usage_cost
            
            # Calculate VAT
            vat_amount = subtotal * VAT_RATE
            total_with_vat = subtotal + vat_amount
            
            invoice = {
                "tenant_id": tenant_id,
                "period": period,
                "invoice_date": datetime.now().isoformat(),
                "base_cost": float(base_cost),
                "usage_cost": float(usage_cost),
                "subtotal": float(subtotal),
                "vat_rate": float(VAT_RATE),
                "vat_country": VAT_COUNTRY,
                "vat_amount": float(vat_amount),
                "total_cost": float(total_with_vat),
                "usage_stats": usage_stats,
                "plan": tenant_plan["name"],
                "status": "pending"
            }
            
            logger.info(f"Invoice generated: {tenant_id}, €{total_with_vat} (incl. VAT)")
            return invoice
        except Exception as e:
            logger.error(f"Failed to generate invoice: {e}")
            return {}
    
    def get_billing_summary(self, tenant_id: str) -> Dict[str, Any]:
        """Get billing summary for tenant"""
        try:
            tenant_plan = self.get_pricing_plan("professional")  # Default plan
            
            from usage_analytics import usage_tracker
            if usage_tracker:
                usage_stats = usage_tracker.get_usage_stats(tenant_id, period="30d")
                usage_cost = self.calculate_usage_cost(tenant_id, usage_stats)
            else:
                usage_cost = Decimal("0.0")
                usage_stats = {}
            
            # Calculate totals with VAT
            subtotal = Decimal(str(tenant_plan["price"])) + usage_cost
            vat_amount = subtotal * VAT_RATE
            total_with_vat = subtotal + vat_amount
            
            summary = {
                "tenant_id": tenant_id,
                "plan": tenant_plan["name"],
                "base_cost": float(Decimal(str(tenant_plan["price"]))),
                "usage_cost": float(usage_cost),
                "subtotal": float(subtotal),
                "vat_rate": float(VAT_RATE),
                "vat_country": VAT_COUNTRY,
                "vat_amount": float(vat_amount),
                "total_cost": float(total_with_vat),
                "usage_stats": usage_stats,
                "limits": {
                    "file_upload_limit": tenant_plan["file_upload_limit"],
                    "storage_limit_gb": tenant_plan["storage_limit_gb"],
                    "api_calls_limit": tenant_plan["api_calls_limit"]
                }
            }
            
            return summary
        except Exception as e:
            logger.error(f"Failed to get billing summary: {e}")
            return {}

# Global billing manager instance
billing_manager = BillingManager()
