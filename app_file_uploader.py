import streamlit as st
from knowledge_base import KnowledgeBaseService
import time


st.title('Welcome to my closes-choosing web with RAG!')
file = st.file_uploader(
    "choose a txt file",
    type=["txt"],
    accept_multiple_files=False,
)

if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()
s = st.session_state['service']

if file is not None:
    file_name = file.name
    file_type = file.type
    file_size = file.size
    file_value = file.getvalue().decode("utf-8")

    st.subheader(f'your file is "{file_name}"')
    st.write(f'file_type: {file_type}|file size: {file_size/1024:.2f} KB')
    st.write(file_value)

    with st.spinner("your file is loading..."):
        time.sleep(1)
        st.write(s.upload_by_str(file_value, file_name))