import streamlit as st
from dotenv import load_dotenv
from agent import Agent

load_dotenv()

st.set_page_config(
    page_title="Careers",
    page_icon=":mortar_board:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.file_uploader("Upload CV")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state.agent.ask_streaming(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})
