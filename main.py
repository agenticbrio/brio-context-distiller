import os
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from openai import AsyncOpenAI

app = FastAPI(title="BRIO Context Distiller API", version="1.0.0")
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

token_usage = {}
FREE_TOKEN_LIMIT = 50000

class DistillRequest(BaseModel):
    text: str
    mode: str = "facts"

def verify_api_key(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API key")
    key = auth.split(" ")[1]
    if key != "brio_test_key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    used = token_usage.get(key, 0)
    if used >= FREE_TOKEN_LIMIT:
        raise HTTPException(status_code=429, detail="Free limit reached. You are processing too much data for a shared API. Contact BRIO to build a dedicated, private Context Distiller LLM inside your own infrastructure.")
    return key

@app.post("/v1/distill")
async def distill_text(data: DistillRequest, api_key: str = Depends(verify_api_key)):
    
    if data.mode == "facts":
        system_prompt = "You are a ruthless context distillation engine. Extract ONLY the core facts, logic, and relationships from the text. Remove all fluff, repetition, greetings, and filler. Output must be dense, highly informational, and structured."
    elif data.mode == "entities":
        system_prompt = "Extract all key entities (people, companies, numbers, dates, technologies) from the text. Return them strictly as a JSON array of objects with 'entity' and 'type' keys. No other text."
    else:
        system_prompt = "Write a 3-sentence executive summary of the core business logic or technical architecture described in this text."

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.text}
            ],
            temperature=0.1
        )
        
        distilled_text = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        token_usage[api_key] = token_usage.get(api_key, 0) + tokens_used
        
        return {
            "status": "success",
            "mode": data.mode,
            "distilled_text": distilled_text,
            "tokens_used": tokens_used,
            "tokens_remaining": FREE_TOKEN_LIMIT - token_usage[api_key]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
