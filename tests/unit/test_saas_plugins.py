import pytest
from packages.shared.saas import SubscriptionTier, TenantQuotaEngine
from packages.tools.plugin_system import BasePlugin, PluginMarketplace
from packages.shared.schemas import RiskLevel

def test_tenant_subscription_quotas():
    # Free tier
    assert TenantQuotaEngine.check_feature_access(SubscriptionTier.FREE, "telephony_calls_enabled") is False
    assert TenantQuotaEngine.check_feature_access(SubscriptionTier.FREE, "computer_control_enabled") is True

    # Premium tier
    assert TenantQuotaEngine.check_feature_access(SubscriptionTier.PREMIUM, "telephony_calls_enabled") is True

def test_plugin_marketplace():
    mp = PluginMarketplace()
    plugin = BasePlugin("github_integration", "1.0.0", "GitHub repository management plugin")
    plugin.register_action("create_issue", "Create GitHub Issue", RiskLevel.MEDIUM, lambda x: True)

    mp.install_plugin(plugin)
    installed = mp.list_installed_plugins()
    assert len(installed) == 1
    assert installed[0]["name"] == "github_integration"
