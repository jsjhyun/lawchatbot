from openai import OpenAI
import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()
import sys
import io
import tiktoken
from loguru import logger

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS

# from streamlit_chat import message
from langchain.callbacks import get_openai_callback
from langchain.memory import StreamlitChatMessageHistory

from streamlit import write
def main():
    st.set_page_config(
    page_title="법률 상담 챗봇",
    page_icon=":books:")

    st.title("💬 법률 상담 챗봇")
    st.caption("A streamlit chatbot powered by OpenAI LLM")
    #sidebar에 OpenAI API key를 입력받는 코드
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"    

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]
    # 이전 대화 기록을 출력해주는 코드
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        for role, message in st.session_state["messages"]:
            st.chat_message(role).write(message)

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
# Chat Logic
    if user_input := st.chat_input("고민 있는 법률 문제를 입력해주세요!"):
        st.chat_message("user").write(user_input)
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
# OpenAI API 호출
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": user_input})

       #AI 응답을 받아오는 코드
        response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        with st.chat_message("assistant"):
            write("상담 내용: " + user_input)
        #AI 응답을 출력해주는 코드
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if __name__ == '__main__':
    main()