# 🗺️ System Architecture Overview

This document outlines the end-to-end technical architecture, system design choices, and data flow patterns implemented across the **EchoHeal AI-Native CRM** ecosystem.

The system is split into **three completely decoupled services** to replicate microservice event-driven handling in modern enterprise notification platforms (e.g., Twilio, WhatsApp Business API).

---

## 🏗️ Core Structural Subsystems
```mermaid
graph TD
    %% Nodes
    UI[Streamlit Frontend <br> Control Dashboard]
    Backend[FastAPI Core CRM <br> main.py : Port 8000]
    Simulator[Independent Simulator <br> channel_service.py : Port 8001]
    AI[Groq LLM API <br> Recovery Agent]

    %% Connections
    UI -->|HTTP REST API JSON| Backend
    Backend -->|HTTP POST Payload| Simulator
    Simulator -->|Asynchronous Webhook Callback <br> POST /api/webhooks/receipt| Backend
    Backend -->|Wake Up Node on Failure| AI
    AI -->|Return Rewritten Copy| Backend
    
    %% Styling
    style UI fill:#2A2D34,stroke:#4f83cc,stroke-width:2px,color:#fff
    style Backend fill:#2A2D34,stroke:#4caf50,stroke-width:2px,color:#fff
    style Simulator fill:#2A2D34,stroke:#ff9800,stroke-width:2px,color:#fff
    style AI fill:#2A2D34,stroke:#9c27b0,stroke-width:2px,color:#fff

### 1. Presentation Layer (`crm_frontend/`)
* **Technology Stack:** Streamlit Cloud.
* **Responsibilities:** Exposes the multi-stage executive control panel (Dashboard, Customer Explorer, Segment Analyzer, AI Studio, and Campaign Launcher).
* **Fault-Tolerance Mechanism:** Implements an automated preflight infrastructure connection handler using asynchronous HTTP health pings. This handles backend container warm-up latency gracefully without allowing network timeout drop-outs to display corrupted empty data blocks to end-users.

### 2. Core Orchestration Engine (`crm_backend/main.py`)
* **Technology Stack:** FastAPI / Uvicorn running on Port `8000`.
* **Responsibilities:** Manages volatile global in-memory transaction states, routes CRM analytical workflows, tracks baseline delivery metrics (`DATA_LOGS`), maintains structural metadata models, and handles the centralized incoming webhook processing routing pipeline.

### 3. Asynchronous Messaging Gateway (`channel_service/channel_service.py`)
* **Technology Stack:** FastAPI / Uvicorn running on Port `8001`.
* **Responsibilities:** Stubs the external delivery communication provider network. When invoked, it instantly sheds execution overhead by responding with an immediate `202 HTTP ACCEPTED` status code back to the core API thread. It passes the operational load natively onto non-blocking background workers using `FastAPI.BackgroundTasks` to evaluate delivery state transitions.

---

## 🔄 End-to-End Campaign Lifecycle Data Flow
[ Frontend ]               [ Core Backend:8000 ]           [ Channel Service:8001 ]       [ Groq LLM API ]
|                               |                                |                          |
|---- 1. Launch Campaign ------>|                                |                          |
|                             (Clears memory arrays)            |                          |
|                               |---- 2. Dispatch Payload ------>|                          |
|                               |     (HTTP client.post)         |                          |
|                               |<--- 3. Ack HTTP 202 (Queued) --|                          |
|                               |                                |                          |
|                               |                                | (Executes sleep(0) &     |
|                               |                                |  runs flat random math)  |
|                               |                                |                          |
|                               |<--- 4. Async Webhook Callback -|                          |
|                               |     (Status payload delivery)  |                          |
|                               |                                |                          |
|                               | [If status == 'failed']        |                          |
|                               |---------------------------- 5. Wake Up Recovery --------->|
|                               |<--------------------------- 6. Return Rewritten Copy ----|
|                               | (Saves self-healing logs)      |                          |
|                               |                                |                          |

1. **Campaign Triggering:** The user initiates a message launch broadcast from the Streamlit UI. The payload transfers a campaign identity string, the core target text string, and the preferred distribution channel to `/api/campaigns/launch`.
2. **Asynchronous Handshake Handoff:** The CRM backend iterates through the targeted user profiles, generates structural placeholder entry indexes mapping inside the data log matrix, and issues structured HTTP POST payloads tracking a unified communication identifier string forward to the messaging gateway container thread.
3. **Task Queue Allocation:** The distribution gateway immediately registers the request payload, asserts structural field compatibility, hands the processing reference off onto execution threads, and terminates the active HTTP connection by returning a native execution receipt validation block.
4. **Bi-Directional Status Webhook Update:** The network simulator resolves operational simulation scenarios matching targeted system distribution statistics. Upon state settlement, it opens an isolated connection channel to submit a raw structural outcome updates payload backward through the public secure `/api/webhooks/receipt` ingest interface path.
5. **AI Self-Healing Execution Node:** If an outcome flag evaluates to a terminal `failed` configuration, the ingest controller extracts context metrics from memory models and awakens an internal automated self-healing framework. The pipeline targets fallback channels, constructs prompt parameters containing the baseline communication parameters, and passes execution handling to the Groq processing framework.
6. **State Resynchronization & Serialization:** The returned optimized marketing text variant overrides previous failed database variables, changes tracking statuses to an `ai_rerouted` data classification, updates analytical tracking maps, and logs structural metadata vectors natively into operational dashboard arrays (`AI_AUDITS`).

---

## ⚖️ Scale Assumptions & Technical Tradeoffs

As an engineered prototype focused on showcasing rapid architecture agility, clear system choices were deliberately balanced against standard enterprise infrastructure overhead:

* **Volatile In-Memory Operations vs. Relational Durability:** System transactions are processed natively inside volatile global state vectors to maximize data execution speed and remove database driver configuration blockers. *At commercial scale, these layers would be backed by an enterprise relational cluster (such as PostgreSQL) decoupled via an asynchronous Object-Relational Mapper (ORM) layer like SQLAlchemy.*
* **Synchronous Loop Execution vs. Decoupled Message Brokers:** Core customer lists are walked directly inside standard loops making web service calls. *In high-throughput corporate ecosystems handling hundreds of thousands of concurrent profiles, these payloads would be safely written directly onto durable horizontal event streamer arrays like Apache Kafka or distributed worker clusters like Celery backed by RabbitMQ.*