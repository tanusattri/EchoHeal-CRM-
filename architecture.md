# Architecture Overview — EchoHeal AI CRM

> **A distributed AI-powered CRM platform that combines customer analytics, intelligent segmentation, campaign orchestration, delivery simulation, and AI-driven self-healing workflows.**

EchoHeal is designed as a modular CRM ecosystem where multiple services collaborate to automate customer engagement campaigns while continuously monitoring delivery outcomes and recovering from failures through AI-generated fallback strategies.

---

# High-Level Architecture

```text
                    ┌────────────────────┐
                    │     Streamlit UI   │
                    │    Frontend Layer  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ FastAPI CRM Backend│
                    │ Business Logic API │
                    └─────────┬──────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ Customer DB │   │ Groq LLM AI │   │ Analytics   │
   │ In-Memory   │   │ Intelligence│   │ Engine      │
   └─────────────┘   └─────────────┘   └─────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Channel Service    │
                    │ Delivery Simulator │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Delivery Webhook   │
                    │ Status Feedback    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ AI Self-Healing    │
                    │ Recovery Engine    │
                    └────────────────────┘
```

---

# System Components

EchoHeal follows a service-oriented architecture where each component owns a specific responsibility.

---

# 1. Frontend Layer

### Technology

* Streamlit

### Responsibilities

* Customer analytics visualization
* Customer explorer
* Segment explorer
* AI Studio
* Campaign launcher
* Delivery monitoring
* Recovery tracking

### Tabs

```text
Dashboard
Customers
Segments
AI Studio
Campaign Center
```

The frontend never directly communicates with AI providers or channel infrastructure.

All communication passes through the backend API.

---

# 2. CRM Backend

### Technology

* FastAPI
* Python

### Responsibilities

* Customer data management
* Campaign orchestration
* Segment generation
* AI workflow management
* Delivery tracking
* Recovery audit logging

The backend acts as the central brain of the entire platform.

---

# Backend API Layer

```text
/api/analytics/overview

/api/customers

/api/orders

/api/segments/inactive

/api/segments/high-value

/api/segments/winter-buyers

/api/copilot

/api/audience-builder

/api/campaigns/launch

/api/dashboard/data

/api/webhooks/receipt
```

Each endpoint is designed around a specific CRM capability.

---

# 3. AI Copilot Engine

### Purpose

Assist marketing teams in generating campaign strategies.

### Flow

```text
User Prompt
      │
      ▼
Backend
      │
      ▼
Groq LLM
      │
      ▼
Audience Recommendation
Suggested Channel
Campaign Message
```

Example:

```text
Create a campaign for inactive customers.
```

Output:

```text
Audience:
Inactive customers

Channel:
WhatsApp

Message:
Get 20% off on your next purchase.
```

---

# 4. AI Audience Builder

### Purpose

Generate customer segments using natural language.

### Flow

```text
Customer Dataset
       │
       ▼
Prompt
       │
       ▼
Groq LLM
       │
       ▼
Matching Audience
```

Example:

```text
Customers who spent more than ₹5000 and have not ordered in 60 days.
```

Output:

```text
Priya Sharma
Rahul Verma
Amit Singh
```

---

# 5. Campaign Orchestration Engine

### Purpose

Launch campaigns across communication channels.

### Supported Channels

```text
WhatsApp
SMS
Email
RCS
```

### Campaign Flow

```text
Campaign Creation
       │
       ▼
Backend
       │
       ▼
Customer Selection
       │
       ▼
Message Generation
       │
       ▼
Channel Service
```

Every campaign generates delivery logs that are later monitored by the dashboard.

---

# 6. Channel Service

### Technology

* FastAPI
* Async Background Tasks

### Purpose

Simulate real-world communication providers.

### Responsibilities

* Accept campaign messages
* Queue messages
* Simulate delivery delays
* Simulate failures
* Generate delivery receipts

---

# Delivery Simulation Logic

```text
Message Sent
      │
      ▼
Delay Simulation
      │
      ▼
Random Outcome
```

Possible outcomes:

```text
Delivered
Read
Clicked
Failed
```

This mimics real-world CRM delivery systems.

---

# 7. Webhook Communication Layer

The Channel Service communicates back to the CRM Backend using webhooks.

### Flow

```text
Channel Service
       │
       ▼
Webhook Event
       │
       ▼
CRM Backend
       │
       ▼
Dashboard Update
```

Example:

```json
{
  "communication_id": "101",
  "status": "delivered"
}
```

This creates real-time delivery tracking behavior.

---

# 8. AI Self-Healing Engine

### Purpose

Automatically recover failed customer communications.

When delivery fails, EchoHeal does not simply stop.

Instead, the system invokes an AI Recovery Agent.

---

# Recovery Workflow

```text
Message Failure
      │
      ▼
Webhook Received
      │
      ▼
AI Recovery Agent
      │
      ▼
Message Rewrite
      │
      ▼
Fallback Channel Selection
      │
      ▼
Recovery Logged
```

---

# Example

Original:

```text
WhatsApp:
Get 20% OFF today.
```

Failure:

```text
Carrier Routing Failure
```

AI Recovery:

```text
SMS:
Exclusive Offer! Enjoy 20% OFF today.
Reply YES to claim.
```

---

# Recovery Audit System

Every recovery attempt is stored.

```text
Customer Name

Failed Channel

Failure Reason

Fallback Channel

AI Generated Message
```

These entries appear inside the Recovery Center dashboard.

---

# Data Flow Architecture

```text
Frontend
    │
    ▼
CRM Backend
    │
    ├────────► Customer Data
    │
    ├────────► AI Copilot
    │
    ├────────► Audience Builder
    │
    └────────► Campaign Launch
                    │
                    ▼
            Channel Service
                    │
                    ▼
           Delivery Outcome
                    │
                    ▼
             Webhook Event
                    │
                    ▼
             CRM Backend
                    │
                    ▼
         AI Self-Healing Engine
                    │
                    ▼
            Dashboard Update
```

---

# Deployment Architecture

```text
                    Internet
                        │
                        ▼

      ┌───────────────────────────────┐
      │ Streamlit Cloud Frontend      │
      └───────────────┬───────────────┘
                      │
                      ▼

      ┌───────────────────────────────┐
      │ Render FastAPI Backend        │
      └───────────────┬───────────────┘
                      │
                      ▼

      ┌───────────────────────────────┐
      │ Render Channel Service        │
      └───────────────────────────────┘
```

This separation enables independent scaling and deployment of services.

---

# Design Principles

### Separation of Concerns

Every service owns a specific responsibility.

### Asynchronous Processing

Delivery events occur independently from campaign creation.

### AI-Augmented CRM

AI assists strategy generation, audience creation, and communication recovery.

### Event-Driven Architecture

Webhook events drive delivery updates and recovery actions.

### Extensible Design

New communication channels and AI agents can be added without redesigning the system.

---

# End-to-End User Journey

```text
User Creates Campaign
          │
          ▼
Campaign Sent
          │
          ▼
Channel Service Processes Messages
          │
          ▼
Delivery Status Generated
          │
          ▼
Webhook Updates CRM
          │
          ▼
Failure Detected
          │
          ▼
AI Self-Healing Activated
          │
          ▼
Fallback Strategy Generated
          │
          ▼
Recovery Logged
          │
          ▼
Dashboard Updated
```

---

# Final Architecture Summary

EchoHeal demonstrates how modern CRM platforms can combine analytics, automation, AI reasoning, event-driven communication, and self-healing workflows into a unified customer engagement system.

Rather than functioning as a simple campaign sender, EchoHeal acts as an intelligent CRM orchestration platform capable of monitoring communication health, adapting to failures, and continuously improving customer outreach through AI-powered decision making.