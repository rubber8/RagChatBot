import streamlit as st
import config_data as config
from rag import RagService


st.title('AI客服为您服务',text_alignment = 'center')
st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "service" not in st.session_state:
    st.session_state["service"] = RagService()


st.chat_message('assistant').write("您好，请问有什么可以帮助您的？")
for sth in st.session_state["messages"]:
    st.chat_message(sth["role"]).write(sth["message"])


prompt = st.chat_input()
if prompt:
    st.chat_message('user').write(prompt)
    st.session_state["messages"].append({"role": "user", "message": prompt})

    stream_list = []
    with st.spinner("AI助手思考中..."):
        res_stream = st.session_state["service"].chain.stream({"input": prompt}, config.session_config)

        def capture(generator,lst):
            for chunk in generator:
                lst.append(chunk)
                yield chunk

        st.chat_message('assistant').write_stream(capture(res_stream,stream_list))
        st.session_state["messages"].append({"role": "assistant", "message": "".join(stream_list)})
