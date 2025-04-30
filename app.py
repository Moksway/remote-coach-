import os
import streamlit as st
from openai import OpenAI
from openai.error import RateLimitError, AuthenticationError, OpenAIError

# ── 1) Page config must come first ───────────────────────────────────────
st.set_page_config(
    page_title="Remote Career Coach",
    layout="centered",
)

# ── 2) Title & description ───────────────────────────────────────────────
st.title("🤖 AI-Driven Remote Career Coach")
st.write(
    "Tell me about your current role, experience, and your goals for remote work—"
    "I’ll give you a personalized roadmap!"
)

# ── 3) Load API key ──────────────────────────────────────────────────────
# Try Streamlit secrets first, then fallback to env var:
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(
        "❌ OpenAI API key not found. "
        "Please set OPENAI_API_KEY in your Streamlit secrets or environment."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# ── 4) Career-coach function ─────────────────────────────────────────────
def get_career_advice(prompt: str) -> str | None:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert remote career coach. "
                "Based on the user's background and goals, "
                "provide tailored advice on remote job paths, "
                "skill development, application strategies, and resources."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",  # cheaper and readily available
            messages=messages,
            max_tokens=400,
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except RateLimitError:
        st.error("⚠️ Rate limit reached. Please try again later.")
    except AuthenticationError:
        st.error("⚠️ Invalid API key. Check your secrets or env var.")
    except OpenAIError as e:
        st.error(f"⚠️ OpenAI error: {e}")
    return None

# ── 5) User input & button ───────────────────────────────────────────────
user_input = st.text_area("Your background & goals", height=200)
if st.button("Get Advice"):
    if not user_input.strip():
        st.warning("Please share some details about yourself.")
    else:
        with st.spinner("Generating your roadmap…"):
            advice = get_career_advice(user_input)
        if advice:
            st.subheader("💼 Your Personalized Roadmap")
            st.write(advice)
