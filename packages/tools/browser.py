import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("switch.tools.browser")

class BrowserEngine:
    def __init__(self):
        self._browser = None
        self._page = None

    async def open_url(self, url: str) -> Dict[str, Any]:
        """Navigate to specified web page URL."""
        logger.info(f"Browser Engine opening URL: '{url}'")
        try:
            from playwright.async_api import async_playwright
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            title = await page.title()
            content = await page.content()
            return {
                "success": True,
                "url": url,
                "title": title,
                "content_preview": content[:1500],
            }
        except Exception as e:
            logger.warning(f"Playwright fallback processing for URL '{url}': {e}")
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=10.0)
                return {
                    "success": True,
                    "url": url,
                    "status_code": resp.status_code,
                    "content_preview": resp.text[:1500],
                }

    async def extract_page_text(self, url: str) -> Dict[str, Any]:
        """Extract clean text content from web page."""
        res = await self.open_url(url)
        return {
            "success": True,
            "url": url,
            "extracted_text": res.get("content_preview", ""),
        }
