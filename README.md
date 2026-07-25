# BRIO Context Distiller API

Stop overpaying for LLM context windows. BRIO strips out fluff, repetition, and filler, returning only the core facts, logic, and relationships.

Built for developers who need to feed massive documents into LLMs without hitting token limits.

## Features
- **Fact Extraction:** Extracts only the core logic and relationships.
- **Entity Extraction:** Returns a clean JSON array of people, companies, and numbers.
- **Executive Summary:** 3-sentence summaries of massive texts.

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/distill` | Compress and extract value from text |

## Quick Start
```bash
curl -X POST https://your-url.com/v1/distill \
-H "Authorization: Bearer brio_test_key" \
-H "Content-Type: application/json" \
-d '{"text": "Paste 10,000 words here...", "mode": "facts"}'
```

## Built by BRIO
BRIO builds highly advanced API infrastructure.
