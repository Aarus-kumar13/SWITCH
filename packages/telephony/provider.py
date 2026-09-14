import os
import uuid
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from packages.shared.schemas import PhoneCallRequest

logger = logging.getLogger("switch.telephony.provider")

class TelephonyProvider(ABC):
    @abstractmethod
    async def initiate_call(self, call_request: PhoneCallRequest) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def handle_voice_webhook(self, payload: Dict[str, Any]) -> str:
        pass


class TwilioTelephonyProvider(TelephonyProvider):
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_phone = os.getenv("TWILIO_PHONE_NUMBER")
        self.enabled = bool(self.account_sid and self.auth_token and self.from_phone)

        if self.enabled:
            from twilio.rest import Client
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None

    async def initiate_call(self, call_request: PhoneCallRequest) -> Dict[str, Any]:
        call_id = f"call_{uuid.uuid4().hex[:8]}"
        logger.info(f"Initiating Phone Call to {call_request.to_phone_number} (ID: {call_id})")

        if not self.enabled:
            logger.warning("Twilio API credentials not configured. Simulating phone call session.")
            return {
                "success": True,
                "call_sid": call_id,
                "status": "queued",
                "simulated": True,
                "message": f"Simulated call initiated to {call_request.to_phone_number}. Context: {call_request.context_summary}",
            }

        try:
            # Generate TwiML Webhook URL
            web_url = os.getenv("WEB_FRONTEND_URL", "http://localhost:8000")
            twiml_url = f"{web_url}/api/phone/twiml?context={call_request.context_summary[:50]}"
            
            call = self.client.calls.create(
                to=call_request.to_phone_number,
                from_=self.from_phone,
                url=twiml_url,
            )
            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "simulated": False,
            }
        except Exception as e:
            logger.error(f"Error initiating Twilio phone call: {e}")
            return {"success": False, "error": str(e), "simulated": False}

    async def handle_voice_webhook(self, payload: Dict[str, Any]) -> str:
        """Generate TwiML response for voice interaction."""
        speech_result = payload.get("SpeechResult", "")
        if speech_result:
            return (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Response>'
                f'<Say>I received your instruction: "{speech_result}". Returning to computer agent to execute and verify.</Say>'
                '</Response>'
            )
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Response>'
            '<Say>Hello! This is SWITCH, your personal AI operating system. How can I help you right now?</Say>'
            '<Gather input="speech" timeout="5"/>'
            '</Response>'
        )
