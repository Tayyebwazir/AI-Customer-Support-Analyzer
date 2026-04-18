import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# ─── Groq Client ───────────────────────────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert AI customer support analyst.

Your job is to analyze a customer message and return a JSON object with exactly these three fields:

1. "category": Classify the message into ONE of these categories only:
   - Complaint
   - Refund/Return
   - Sales Inquiry
   - Delivery Question
   - Account/Technical Issue
   - General Query
   - Spam

2. "sentiment": Identify the emotional tone as exactly ONE of:
   - Positive
   - Neutral
   - Negative

3. "auto_reply": Write a short (2-4 sentences), professional, empathetic auto-reply
   appropriate for the message. Sound human and helpful.

STRICT RULES:
- Return ONLY valid JSON. No explanation, no markdown, no extra text.
- Do not wrap the JSON in code blocks.
- Example output format:
{
  "category": "Complaint",
  "sentiment": "Negative",
  "auto_reply": "We sincerely apologize for the inconvenience you've experienced. Our support team will look into this immediately and get back to you within 24 hours."
}
"""

# ─── Main Analysis Function ────────────────────────────────────────────────────
def analyze_message(customer_message: str) -> dict:
    """
    Send a customer message to Groq (LLaMA 3) and return:
    {
        "category": str,
        "sentiment": str,
        "auto_reply": str
    }
    Returns {"error": str} on failure.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Free & powerful Groq model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Customer message: {customer_message}"},
            ],
            temperature=0.3,       # Low temp = consistent, structured output
            max_tokens=300,
        )

        raw_text = response.choices[0].message.content.strip()

        # Clean up in case model wraps in markdown code fences
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        result = json.loads(raw_text)

        # Validate keys
        required_keys = {"category", "sentiment", "auto_reply"}
        if not required_keys.issubset(result.keys()):
            return {"error": "Incomplete response from AI. Missing fields."}

        # Validate allowed values
        valid_categories = {
            "Complaint", "Refund/Return", "Sales Inquiry",
            "Delivery Question", "Account/Technical Issue",
            "General Query", "Spam"
        }
        valid_sentiments = {"Positive", "Neutral", "Negative"}

        if result["category"] not in valid_categories:
            result["category"] = "General Query"   # fallback

        if result["sentiment"] not in valid_sentiments:
            result["sentiment"] = "Neutral"         # fallback

        return result

    except json.JSONDecodeError:
        return {"error": "AI returned invalid JSON. Please try again."}
    except Exception as e:
        return {"error": str(e)}
    
    