from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from packages.shared.schemas import PhoneCallRequest

router = APIRouter(prefix="/api/phone", tags=["phone"])

@router.post("/call")
async def trigger_outbound_call(payload: dict):
    from main import telephony_provider
    phone_number = payload.get("to_phone_number", "+1987654321")
    context = payload.get("context_summary", "Technical deployment notification")
    initial_speech = payload.get("initial_speech", "Hello! This is SWITCH calling regarding your deployment.")

    req = PhoneCallRequest(
        to_phone_number=phone_number,
        context_summary=context,
        initial_speech=initial_speech,
    )
    result = await telephony_provider.initiate_call(req)
    return result

@router.post("/twiml")
async def handle_twiml_webhook(request: Request):
    from main import telephony_provider
    form_data = await request.form()
    twiml_xml = await telephony_provider.handle_voice_webhook(dict(form_data))
    return Response(content=twiml_xml, media_type="application/xml")
