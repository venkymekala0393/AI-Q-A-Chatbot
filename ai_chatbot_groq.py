import streamlit as st
from groq import Groq
import os

# Get API key securely
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found!")
    st.info("Please add your Groq API key in Streamlit secrets.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(
    page_title=" 🤖 Q&A Chatbot ",
    layout="centered"
)

st.title(" 🤖 Q&A Chatbot")
st.write("Ask any question")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a factual Q&A assistant. "
                        "Give clear and concise answers. "
                        "If you do not know the answer, say 'I don't know'. "
                        "Do not hallucinate."
                    )
                },
                *st.session_state.messages
            ],
            temperature=0.2
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



