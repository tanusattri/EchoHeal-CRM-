import os
import random
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from customer import CUSTOMERS
from customer import ORDERS

from ai_agent import ask_groq

from pydantic import BaseModel
import httpx
load_dotenv()

app = FastAPI(
    title="EchoHeal AI CRM Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


DATA_LOGS = []
AI_AUDITS = []

# ====================================
# MODELS
# ====================================

class CampaignPayload(BaseModel):
    campaign_name: str
    channel: str
    base_message: str


class CopilotRequest(BaseModel):
    prompt: str

class ReceiptPayload(BaseModel):
    communication_id: str
    status: str
    reason: str | None = None


async def execute_ai_self_healing(
    customer,
    original_message,
    failed_channel,
    failure_reason,
    log_entry
):

    fallback_channel = (
        "SMS"
        if failed_channel == "WhatsApp"
        else "WhatsApp"
    )

    system_prompt = """
    You are an AI CRM Recovery Agent.

    Rewrite the failed marketing message
    for the fallback channel.

    Keep:
    - Offer
    - CTA
    - Meaning

    Return only the final message.
    """

    user_prompt = f"""
    Customer:
    {customer['name']}

    Failed Channel:
    {failed_channel}

    Fallback Channel:
    {fallback_channel}

    Message:
    {original_message}
    """

    try:

        ai_text = await ask_groq(
            system_prompt,
            user_prompt
        )

        log_entry["current_channel"] = fallback_channel
        log_entry["delivery_status"] = "ai_rerouted"
        log_entry["message_body"] = ai_text

        AI_AUDITS.append({

            "customer_name":
                customer["name"],

            "customer_age":
                customer["age"],

            "failed_channel":
                failed_channel,

            "failure_reason":
                failure_reason,

            "fallback_channel":
                fallback_channel,

            "new_message":
                ai_text
        })

        print(
            f"AI Recovery Success -> "
            f"{customer['name']}"
        )

    except Exception as e:

        print(
            f"AI Recovery Error: {str(e)}"
        )

# ====================================
# HEALTH CHECK
# ====================================

@app.get("/")
async def home():

    return {
        "status": "running",
        "service": "EchoHeal CRM Backend"
    }


# ====================================
# DASHBOARD
# ====================================

@app.get("/api/dashboard/data")
async def dashboard():

    return {
        "logs": DATA_LOGS,
        "ai_audit": AI_AUDITS
    }

@app.post("/api/webhooks/receipt")
async def receive_receipt(payload: ReceiptPayload):
    customer_id = int(payload.communication_id)
    customer = next((c for c in CUSTOMERS if c["id"] == customer_id), None)

    if not customer:
        return {"error": "customer not found"}

    log_entry = next((log for log in DATA_LOGS if log["customer_name"] == customer["name"]), None)

    if not log_entry:
        return {"error": "log not found"}

    # Update base status
    log_entry["delivery_status"] = payload.status

    # 🚨 WAKE UP THE AI IF THE CHANNEL FAILED!
    if payload.status == "failed":
        # We trigger the background recovery worker immediately
        await execute_ai_self_healing(
            customer=customer,
            original_message=log_entry["message_body"],
            failed_channel=log_entry["current_channel"],
            failure_reason=payload.reason or "Carrier Drop",
            log_entry=log_entry
        )

    print(f"WEBHOOK UPDATE -> {customer['name']} | {log_entry['delivery_status']}")
    return {"status": "processed"}

# ====================================
# ANALYTICS
# ====================================

@app.get("/api/analytics/overview")
async def analytics():

    revenue = sum(
        order["amount"]
        for order in ORDERS
    )

    inactive = len([
        c for c in CUSTOMERS
        if c["last_order_days"] > 60
    ])

    high_value = len([
        c for c in CUSTOMERS
        if c["total_spend"] > 5000
    ])

    return {
        "customers": len(CUSTOMERS),
        "orders": len(ORDERS),
        "revenue": revenue,
        "inactive_customers": inactive,
        "high_value_customers": high_value
    }


# ====================================
# SEGMENTS
# ====================================

@app.get("/api/segments/inactive")
async def inactive_segment():

    result = []

    for customer in CUSTOMERS:

        if customer["last_order_days"] > 60:
            result.append(customer)

    return {
        "segment": "Inactive Customers",
        "count": len(result),
        "customers": result
    }


@app.get("/api/segments/high-value")
async def high_value_segment():

    result = []

    for customer in CUSTOMERS:

        if customer["total_spend"] > 5000:
            result.append(customer)

    return {
        "segment": "High Value Customers",
        "count": len(result),
        "customers": result
    }


@app.get("/api/segments/winter-buyers")
async def winter_buyers():

    result = []

    for customer in CUSTOMERS:

        if customer["favorite_category"] == "Winter Wear":
            result.append(customer)

    return {
        "segment": "Winter Wear Buyers",
        "count": len(result),
        "customers": result
    }


# ====================================
# AI CRM COPILOT
# ====================================

@app.post("/api/copilot")
async def copilot(req: CopilotRequest):

    system_prompt = """
    You are an AI CRM strategist.

    Return:
    Audience
    Suggested Channel
    Suggested Campaign Message

    Keep response concise.
    """

    result = await ask_groq(
        system_prompt,
        req.prompt
    )

    return {
        "response": result
    }


# ====================================
# AI AUDIENCE BUILDER
# ====================================

@app.post("/api/audience-builder")
async def audience_builder(req: CopilotRequest):

    customers_text = "\n".join([
        f"""
        Name:{c['name']}
        Age:{c['age']}
        Spend:{c['total_spend']}
        LastOrder:{c['last_order_days']}
        Category:{c['favorite_category']}
        """
        for c in CUSTOMERS
    ])

    system_prompt = """
    You are a CRM audience builder.

    Use customer data.

    Return matching customer names.
    """

    result = await ask_groq(
        system_prompt,
        f"""
        Customer Data:
        {customers_text}

        Segment Request:
        {req.prompt}
        """
    )

    return {
        "audience": result
    }


# ====================================
# CAMPAIGN LAUNCH
# ====================================

@app.post("/api/campaigns/launch")
async def launch_campaign(
    payload: CampaignPayload
):

    DATA_LOGS.clear()
    AI_AUDITS.clear()

    async with httpx.AsyncClient() as client:

        for customer in CUSTOMERS:

            log_entry = {

                "communication_id": customer["id"],

                "customer_name": customer["name"],

                "customer_age": customer["age"],

                "current_channel": payload.channel,
                "delivery_status": "queued",

                "message_body":
                    payload.base_message
            }

            DATA_LOGS.append(
                log_entry
            )

            try:

                response= await client.post(

                    "http://127.0.0.1:8001/api/channels/send",

                    json={

                        "communication_id":
                            str(customer["id"]),

                        "recipient_identifier":
                            customer["phone"],

                        "channel":
                            payload.channel,

                        "message_body":
                            payload.base_message
                    },

                    timeout=5
                )
                print(
                    f"Sent to Channel Service | "
                    f"{customer['name']} | "
                    f"Status={response.status_code}"
                )

            except Exception as e:

                log_entry[
                    "delivery_status"
                ] = "failed"

                print(
                    f"Channel Error: {str(e)}"
                )

    return {

        "status":
            "success",

        "campaign":
            payload.campaign_name,

        "customers":
            len(CUSTOMERS)
    }

@app.get("/api/customers")
async def get_customers():

    return CUSTOMERS

@app.get("/api/orders")
async def get_orders():

    return ORDERS

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )