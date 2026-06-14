import asyncio
import os
import random
import httpx

from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi import status

from pydantic import BaseModel

app= FastAPI(
    title="EchoHeal Delivery Simulator",
    version="2.0"
)

RENDER_PORT= os.environ.get("PORT", "8000")
CRM_WEBHOOK_URL= "https://echoheal-backend-v2.onrender.com/api/webhooks/receipt"

class ChannelPayload(BaseModel):
    communication_id: str
    recipient_identifier: str
    channel: str
    message_body: str

async def simulate_delivery(payload: ChannelPayload):
    await asyncio.sleep(0)
    delivery_status = "delivered"
    failure_reason= "None" 
    r= random.random()
    if r<0.15:
        delivery_status= "failed"
        failure_reason= "Carrier Routing Failure"
    elif r< 0.30:
        delivery_status= "failed"
        failure_reason= "Carrier Congestion"
    elif r< 0.65:
        delivery_status= "delivered"
    elif r< 0.85:
        delivery_status= "read"
    else:
        delivery_status= "clicked"

    webhook_payload= {
        "communication_id": payload.communication_id,
        "status": delivery_status,
        "reason": failure_reason
    }

    try:
        async with httpx.AsyncClient() as client:
            response= await client.post(
                CRM_WEBHOOK_URL,
                json=webhook_payload,
                timeout=10
            )

            print(
                f"Webhook Sent -> "
                f"URL: {CRM_WEBHOOK_URL} | "
                f"Status Code: {response.status_code} | "
                f"Delivery: {delivery_status}"
            )

    except Exception as e:
        print(f"Webhook Transmission Crash: {str(e)}")

@app.post(
    "/api/channels/send",
    status_code=status.HTTP_202_ACCEPTED
)
async def send_message(
    payload: ChannelPayload,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        simulate_delivery,
        payload
    )

    return {
        "status": "queued",
        "communication_id": payload.communication_id,
        "channel": payload.channel,
        "recipient": payload.recipient_identifier
    }

@app.get("/")
async def health():
    return {
        "service": "EchoHeal Channel Service",
        "status": "running"
    }

if __name__== "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001
    )
