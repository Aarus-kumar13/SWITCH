import logging
from enum import Enum
from typing import Dict, Any, Optional

logger = logging.getLogger("switch.shared.saas")

class SubscriptionTier(str, Enum):
    FREE = "FREE"
    PRO = "PRO"
    PREMIUM = "PREMIUM"
    BUSINESS = "BUSINESS"


class TenantQuotaEngine:
    TIER_LIMITS = {
        SubscriptionTier.FREE: {
            "max_daily_tasks": 50,
            "computer_control_enabled": True,
            "telephony_calls_enabled": False,
            "custom_plugins_enabled": False,
            "max_memory_items": 100,
        },
        SubscriptionTier.PRO: {
            "max_daily_tasks": 500,
            "computer_control_enabled": True,
            "telephony_calls_enabled": False,
            "custom_plugins_enabled": True,
            "max_memory_items": 1000,
        },
        SubscriptionTier.PREMIUM: {
            "max_daily_tasks": 5000,
            "computer_control_enabled": True,
            "telephony_calls_enabled": True,
            "custom_plugins_enabled": True,
            "max_memory_items": 10000,
        },
        SubscriptionTier.BUSINESS: {
            "max_daily_tasks": 50000,
            "computer_control_enabled": True,
            "telephony_calls_enabled": True,
            "custom_plugins_enabled": True,
            "max_memory_items": 100000,
        },
    }

    @classmethod
    def check_feature_access(cls, tier: SubscriptionTier, feature_name: str) -> bool:
        limits = cls.TIER_LIMITS.get(tier, cls.TIER_LIMITS[SubscriptionTier.FREE])
        return limits.get(feature_name, False)
