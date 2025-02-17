import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="Therapy Bot",
    page_icon="",
    layout="centered"
)

API_KEY = st.secrets["GROQ_API_KEY"]
if not API_KEY:
    st.error("GROQ_API_KEY is missing in Streamlit secrets. Please check your setup.")
    st.stop()

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Therapy Bot")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask Therapy Bot")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": f"""You are an experienced, helpful professional psychological therapist."""},
        *st.session_state.chat_history
    ]

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )
            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant"):
                st.markdown(assistant_response)

        except Exception as e:
            st.error(f"Error while fetching response from Groq: {e}")