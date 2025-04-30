import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# 1. Explicitly load the .env file
env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(env_path)

# 2. ────── MUST be FIRST Streamlit command! ──────────────────────────────────
st.set_page_config(page_title="Remote Career Coach", layout="centered")

# 3. DEBUG: now it’s safe to use st.write


# 4. Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 5. Define the AI coach function
def get_career_advice(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert remote career coach. "
                "Provide tailored advice on remote job paths, skill development, "
                "application strategies, and resources."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",      # or "gpt-4"
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content

# 6. Now build the rest of your UI
st.title("🤖 AI-Driven Remote Career Coach")
st.write("Tell me about your background and goals for remote work:")

user_input = st.text_area("Your background & goals", height=200)
if st.button("Get Advice"):
    if not user_input.strip():
        st.warning("Please share some details first.")
    else:
        with st.spinner("Thinking…"):
            advice = get_career_advice(user_input)
        st.subheader("💼 Your Personalized Roadmap")
        st.write(advice)
