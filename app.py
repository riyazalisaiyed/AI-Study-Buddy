import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
client = genai.Client(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Study Buddy")
st.subheader("Your Personal AI Tutor for 12th Science")

st.write(
    "Ask questions and get explanations from your AI tutor."
)

# Subject selection
subject = st.selectbox(
    "Select Subject",
    [
        "Physics",
        "Chemistry",
        "Mathematics",
        "Biology"
    ]
)

# Question
question = st.text_area(
    "Ask your question",
    placeholder="Example: Explain ionic equilibrium in simple language."
)

uploaded_file = st.file_uploader(
    "📄 Upload your study notes (PDF)",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:
    from pypdf import PdfReader

    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

    st.success(f"Uploaded: {uploaded_file.name}")

    st.info(
        f"PDF contains {len(reader.pages)} pages "
        f"and {len(pdf_text)} characters of text."
    )

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

# Ask AI button
if st.button("🤖 Ask AI"):

    if question.strip():

        prompt = f"""
You are an AI tutor for a 12th Science student.

Subject: {subject}

Student Question:
{question}

Explain the answer in simple and clear language suitable for a 12th Science student.

If appropriate:
- Give a simple explanation
- Give an example
- Show important points
- Use formulas where required
"""

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        st.subheader("📚 AI Tutor Answer")
        st.write(response.text)

    else:
        st.warning("Please enter your question.")