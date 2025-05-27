import streamlit as st
from dotenv import load_dotenv
from agent import Agent
from prompt_message import CHAT_WELCOME_MESSAGE

load_dotenv()

st.set_page_config(
    page_title="Careers",
    page_icon=":mortar_board:",
    layout="centered",
    initial_sidebar_state="expanded",
)

#State
if "files" not in st.session_state:
    st.session_state["files"] = []
if "agent" not in st.session_state:
    st.session_state["agent"] = Agent()  
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": CHAT_WELCOME_MESSAGE}]                                       
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Sidebar
with st.sidebar:
    st.markdown("## Upload CV")
    uploaded_file = st.file_uploader(label="",label_visibility="collapsed", type=["pdf", "docx", "txt"])
    
    st.markdown("## Download files")
    for file in st.session_state["files"]:
        st.download_button(
            label=file["label"],
            data=file["data"],
            file_name=f"{file['file_name']}.pdf",
            mime=file["mime"],
        )
        
#Cv upload
if uploaded_file is not None and st.session_state["agent"].uploaded_cv is None:
    st.session_state["agent"].uploaded_cv = uploaded_file.read()
    prompt= """
        I have just uploaded new CV to your memory. 
        Make sure you note this. 
        Now you must call extract_data_from_pdf function to extract data from file that is stored inside your memory
        """  
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state["agent"].ask_streaming(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})     
elif uploaded_file is None and st.session_state["agent"].uploaded_cv is not None:
    st.session_state["agent"].uploaded_cv = None
    prompt = """
        I have deleted CV from your memory. 
        Now you do not have access to it.
        """ 
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state["agent"].ask_streaming(prompt))


#Chat loop
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state["agent"].ask_streaming(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})  