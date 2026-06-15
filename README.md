# EchoHeal — AI-Powered CRM Campaign Orchestration & Self-Healing Communication Platform

> **An intelligent CRM system that combines audience segmentation, AI campaign generation, multi-channel communication, delivery tracking, and autonomous recovery into a unified customer engagement workflow.**

Built for modern customer engagement platforms, EchoHeal demonstrates how AI can move beyond content generation and actively participate in communication orchestration.

Instead of treating campaign delivery as a one-way process, EchoHeal introduces an adaptive workflow where communication failures are detected, analyzed, and automatically recovered using AI-generated fallback messaging.

---

# Live Demo

### Frontend Application

https://7t34w5hqnsds2xqzeuxa7k.streamlit.app/

### Backend API

https://echoheal-backend-v2.onrender.com

---

# ⚡ Quick Evaluation Guide

**No local setup is required.**

The application is fully deployed and ready to use.

To evaluate the project:

1. Open the Streamlit application.
2. Navigate through Dashboard, Customers, Segments, AI Studio and Campaign Center.
3. Launch a campaign from the Campaign Center.
4. Observe delivery tracking updates.
5. View AI-generated recovery actions for failed communications.

The backend services are already deployed and connected.

Recruiters and reviewers only need to open the Streamlit application to experience the complete workflow.

No backend startup, environment setup, API configuration or local execution is required.

---

# Why EchoHeal?

Modern CRM systems excel at sending campaigns but often struggle when communication breaks.

A failed WhatsApp message, undelivered SMS, or routing failure typically requires manual intervention, leading to lost engagement opportunities and poor customer experiences.

EchoHeal reimagines CRM as an intelligent communication system.

Rather than simply reporting failures, the platform actively responds to them through AI-powered recovery workflows, ensuring customer communication continues even when delivery channels fail.

This creates a more resilient, automated, and adaptive engagement pipeline.

---

# The Problem We Solve

Traditional CRM platforms can:

* Segment customers
* Launch campaigns
* Track deliveries

But they often cannot:

* Adapt to channel failures
* Recover failed communications automatically
* Generate contextual fallback messaging
* Coordinate AI with communication infrastructure
* Simulate real-world delivery workflows

Most CRM systems stop at delivery tracking.

EchoHeal continues beyond delivery.

---

# What Makes EchoHeal Different?

### Traditional CRM Workflow

```text
Campaign Launch
      ↓
Message Sent
      ↓
Delivery Status
      ↓
End
```

### EchoHeal Workflow

```text
Campaign Launch
      ↓
Audience Segmentation
      ↓
Channel Service Delivery
      ↓
Delivery Event Tracking
      ↓
Webhook Processing
      ↓
Failure Detection
      ↓
AI Recovery Agent
      ↓
Fallback Channel Routing
      ↓
Successful Customer Engagement
```

This architecture creates:

* Smarter communication workflows
* Improved campaign resilience
* AI-assisted recovery
* Better customer reachability
* Real-world CRM simulation

---

# Architecture Overview

```text
┌─────────────────────────┐
│     Streamlit UI        │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│     CRM Backend API     │
│       FastAPI           │
└───────────┬─────────────┘
            ↓
 ┌──────────┼──────────┐
 ↓          ↓          ↓
Analytics  AI Studio  Campaign Engine
            ↓
    ┌───────────────────┐
    │   Groq AI Layer   │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │ Channel Service   │
    │ Delivery Engine   │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │ Webhook Events    │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │ AI Self-Healing   │
    └─────────┬─────────┘
              ↓
    ┌───────────────────┐
    │ Recovery Audit    │
    └───────────────────┘
```

---

# Core Features

### AI CRM Copilot

EchoHeal includes an AI-powered CRM strategist capable of generating campaign ideas, audience recommendations, and customer engagement strategies using natural language prompts.

Instead of manually designing campaigns, users can describe their objective and receive AI-generated recommendations.

---

### AI Audience Builder

The Audience Builder transforms natural language descriptions into customer segments.

Examples include:

* High-value customers
* Inactive customers
* Seasonal shoppers
* Behavioral audiences

This enables marketers to create customer groups without manually writing segmentation rules.

---

### Campaign Orchestration Engine

Campaigns can be launched across multiple communication channels.

Supported channels include:

* WhatsApp
* SMS
* Email
* RCS

Each campaign is automatically distributed to the targeted customer base through the communication pipeline.

---

### Delivery Tracking System

EchoHeal tracks every communication event throughout its lifecycle.

Possible states include:

* Queued
* Delivered
* Read
* Clicked
* Failed

This provides visibility into campaign performance and communication health.

---

### Channel Service Simulation

A dedicated delivery service simulates real-world communication networks.

The service introduces:

* Delivery delays
* Random failures
* Engagement events
* Status callbacks

This creates a realistic environment for testing CRM workflows.

---

### AI Self-Healing Communication

The most distinctive feature of EchoHeal.

When communication fails:

1. Delivery failure is detected.
2. A webhook notifies the CRM backend.
3. The AI Recovery Agent is activated.
4. Groq generates a revised message.
5. A fallback communication channel is selected.
6. Communication is restored.

This transforms CRM from a passive tracking system into an adaptive communication platform.

---

### Recovery Audit Center

Every recovery event is recorded for transparency.

The system tracks:

* Failed channel
* Failure reason
* Fallback channel
* AI-generated recovery message

This creates a complete audit trail for communication recovery.

---

# Project Structure

```bash
echoheal/
│
├── frontend/
│   └── app.py
│
├── backend/
│   ├── main.py
│   ├── ai_agent.py
│   ├── customer.py
│
├── channel_service/
│   └── main.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# Meet The Components

## Streamlit Frontend

The presentation layer of the system.

### Responsibilities

* Dashboard visualization
* Customer exploration
* Audience generation
* Campaign management
* Recovery monitoring

---

## CRM Backend

The orchestration engine.

### Responsibilities

* Campaign execution
* Customer segmentation
* Webhook processing
* Delivery tracking
* AI integration

### Powered By

* FastAPI

---

## AI Copilot

The strategic intelligence layer.

### Responsibilities

* Campaign planning
* Marketing recommendations
* Audience suggestions
* CRM guidance

### Powered By

* Groq API

---

## AI Recovery Agent

The self-healing engine.

### Responsibilities

* Failure analysis
* Message rewriting
* Fallback routing
* Communication recovery

### Powered By

* Groq API

---

## Channel Service

The delivery simulation layer.

### Responsibilities

* Message processing
* Delivery simulation
* Event generation
* Webhook callbacks

### Powered By

* FastAPI Background Tasks

---

# Tech Stack

### Frontend

* Streamlit
* Pandas

### Backend

* FastAPI
* Pydantic
* HTTPX

### AI

* Groq API
* Llama Models

### Architecture

* Microservices
* Async Processing
* Event-Driven Communication
* Webhook-Based Integration

---

# Installation

# Running The Project Locally (Optional)

The application is already deployed and can be evaluated directly through the live demo.

### Live Application

Frontend:

https://7t34w5hqnsds2xqzeuxa7k.streamlit.app/

Backend:

https://echoheal-backend-v2.onrender.com

---

## Local Setup (For Developers)

### Clone Repository

```bash
git clone <your-repository-url>
cd echoheal
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
```

### Start Backend

```bash
uvicorn main:app --reload
```

### Start Channel Service

```bash
uvicorn channel_service:app --reload --port 8001
```

### Start Frontend

```bash
streamlit run app.py
```

# Future Scope

EchoHeal is designed as a foundation for intelligent CRM infrastructure.

Future enhancements may include persistent databases, real-time WebSocket dashboards, predictive failure detection, customer-level personalization, campaign analytics, distributed channel routing, and autonomous communication optimization.

These additions would transform EchoHeal from a CRM simulation platform into a production-grade AI communication orchestration system.

---

# Contribution

Contributions are welcome.

### How To Contribute

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit updates
5. Open a pull request

---

# License

MIT License

---

# Final Thought

EchoHeal demonstrates how customer engagement systems become significantly more powerful when communication is treated as a dynamic process rather than a static delivery task.

By combining AI reasoning, delivery simulation, webhook-driven workflows, and autonomous recovery, the platform showcases how future CRM systems can move beyond tracking communication and begin actively managing it.

Rather than functioning as a simple campaign tool, EchoHeal represents a step toward intelligent, resilient, and self-healing customer engagement infrastructure.

> Built to explore the future of AI-driven communication orchestration.

# Deployment

### Frontend

Deployed on Streamlit Cloud

https://7t34w5hqnsds2xqzeuxa7k.streamlit.app/

### Backend

Deployed on Render

https://echoheal-backend-v2.onrender.com

### Architecture

```text
Streamlit Frontend
        ↓
Render FastAPI Backend
        ↓
Groq AI Layer
        ↓
Campaign Engine
        ↓
Delivery Tracking
        ↓
AI Self-Healing Workflow
```

The deployed version is fully functional and ready for evaluation.
