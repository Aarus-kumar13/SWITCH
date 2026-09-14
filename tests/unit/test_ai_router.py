import pytest
from packages.ai.router import AIRouter
from packages.shared.schemas import ModelCategory

@pytest.mark.asyncio
async def test_ai_router_fallback():
    router = AIRouter()
    res = await router.route_and_generate(
        prompt="Test system query",
        category=ModelCategory.REASONING,
    )
    assert res is not None
    assert len(res) > 0
