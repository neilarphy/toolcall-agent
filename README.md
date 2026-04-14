# DevAssist

A coding assistant for the development team. Answers questions, reads files, and runs shell commands to help with day-to-day engineering tasks.

## Setup

```bash
cp .env.example .env
# Add your GEMINI_API_KEY
docker-compose up -d
```

## API

OpenAI-compatible endpoint:

```
POST /v1/chat/completions
GET  /health
DELETE /sessions/{session_id}
```

## Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What files are in the current directory?"}]}'
```
