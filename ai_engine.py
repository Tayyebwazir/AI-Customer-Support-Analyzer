import os
import json
import streamlit as st  # <-- ADD THIS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Use Streamlit Secrets for the API Key if deployed, otherwise use env
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are an expert AI customer support analyst.
Return ONLY valid JSON with fields: "category", "sentiment", "auto_reply".
"""

def analyze_message(customer_message: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Customer message: {customer_message}"},
            ],
            temperature=0.3,
        )
        raw_text = response.choices[0].message.content.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_text)
    except Exception as e:
        return {"error": str(e)}

# ─── STREAMLIT UI (This is what fixes the "Blue Circle") ──────────────────
st.title("📩 AI Customer Support Analyzer")
st.write("Enter a customer message below to analyze sentiment and generate a reply.")

user_input = st.text_area("Customer Message:", placeholder="e.g., My order hasn't arrived yet!")

if st.button("Analyze Message"):
    if user_input:
        with st.spinner("Analyzing..."):
            result = analyze_message(user_input)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.subheader("Analysis Results")
                col1, col2 = st.columns(2)
                col1.metric("Category", result.get("category"))
                col2.metric("Sentiment", result.get("sentiment"))
                
                st.write("**Suggested Auto-Reply:**")
                st.info(result.get("auto_reply"))
    else:
        st.warning("Please enter a message first!")
