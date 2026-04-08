# Content Moderation Environment

## Overview

The **Content Moderation Environment** simulates real-world content moderation tasks for AI agents.

Agents receive a post with **content, context, and intent**, and must decide:

- `allow` → content is safe to publish  
- `remove` → content violates rules and should be removed  
- `review` → content requires human review  

The environment evaluates the agent’s decision against a ground-truth label and returns a reward in the range **0.0–1.0**, enabling incremental learning and partial credit for ambiguous cases.

Each episode consists of a **single moderation decision**.

This environment is **containerized** and fully compatible with **OpenEnv**, ready to deploy as a **Hugging Face Space**.

---

## Features

- Supports concurrent sessions
- Typed models for actions and observations
- Meaningful reward function:
  - Correct decision → `1.0`
  - Review decision → `0.5`
  - Incorrect decision → `0.0`
- Three task difficulties: **easy → medium → hard**
- Baseline inference script produces reproducible scores
- Containerized deployment via **Docker** and **Hugging Face Spaces**

---

## Task Descriptions

### Easy Tasks
Simple appreciation, praise, or minor insults.

**Example:**
```
Content: "This explanation made everything so much easier to understand!"
Context: "comment on tutorial video"
Intent: "positive appreciation"
Correct Action: allow
```

---

### Medium Tasks
Contains criticism or slang, may be ambiguous.

**Example:**
```
Content: "This is honestly a very poor attempt."
Context: "feedback after submission"
Intent: "harsh criticism"
Correct Action: review
```

---

### Hard Tasks
Sarcasm, jokes with violent language, or subtle threats.

**Example:**
```
Content: "If you mess this up again, I swear I'll kill you 😂"
Context: "friends joking during online game"
Intent: "joking with violent language"
Correct Action: review
```

---

## Action & Observation Spaces

### Action Space

| Field    | Type | Description                          |
|----------|------|--------------------------------------|
| decision | str  | allow, remove, review                |

### Observation Space

| Field   | Type | Description                          |
|--------|------|--------------------------------------|
| content | str  | Text content to be moderated         |
| context | str  | Context in which content appears     |
| intent  | str  | Intended meaning of the content      |

---

## Setup & Usage

### Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- Hugging Face account & API token

---

### Local Development

```bash
# Clone repository
git clone <repo-url>
cd OpenEnv

# Install dependencies
pip install -r requirements.txt

# Run environment server locally
python -m content_moderation.server.app

# OR using uvicorn
uvicorn content_moderation.server.app:app --reload --host 0.0.0.0 --port 8000
```

---

### Using Docker

```bash
# Build Docker image
docker build -t content-moderation-env .

# Run container
docker run -p 8000:8000 content-moderation-env
```

Verify server:

```
http://localhost:8000/health
```

---

## OpenEnv Integration

### API Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| POST   | /reset  | Reset environment |
| POST   | /step   | Execute action |
| GET    | /state  | Retrieve current environment state |
| GET    | /schema | Retrieve action & observation schemas |
| WS     | /ws     | WebSocket endpoint for persistent sessions |

---

### Example: Inference Script

```bash
python -m content_moderation.server.inference
```

**Sample Logs:**
```
[START] task=content_moderation env=content_moderation model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=allow reward=1.00 done=true error=null
[END] success=true steps=1 score=1.00 rewards=1.00
```

---

## Hugging Face Space Deployment

- Runtime: `fastapi`
- App: `server.app:app`
- Port: `8000`
- OpenEnv spec version: `1`
- Environment type: `space`

### Required Environment Variables

| Variable      | Description                     |
|--------------|---------------------------------|
| API_BASE_URL | LLM API endpoint                |
| MODEL_NAME   | Model identifier for inference  |
| HF_TOKEN     | Hugging Face API token          |

---

## Deployment (Docker)

```bash
docker build -t content-moderation-env .
docker run -p 8000:8000 content-moderation-env
```

Check health endpoint:

```bash
curl http://localhost:8000/health
```

---

## Baseline Scores

- Easy tasks → `1.0` reward
- Medium tasks → `0.5–1.0` reward (depending on ambiguity)
- Hard tasks → `0.0–1.0` reward (depending on sarcasm or threats)

The baseline inference script completes successfully with **reproducible scores**.

---

## License

This project is licensed under a **BSD-style license**. See the `LICENSE` file for details.
