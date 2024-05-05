import streamlit as st
import tiktoken
from loguru import logger
# from retriever import rag_func
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
# from chatbot.main import get_conversation_chain, get_text, get_text_chunks, get_vectorstore
from langchain_community.vectorstores import FAISS
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.runnables import RunnablePassthrough
from prompt import get_prompt
<<<<<<<<< Temporary merge branch 1
from retriever import *
from multiple_retriever import *
=========
>>>>>>>>> Temporary merge branch 2

def main():
    st.set_page_config(
    page_title="law chat",
    page_icon=":books:")

    st.title("💬 법률 상담 챗봇")
    st.caption("쉽고, 편리한 법률 상담")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


    with st.sidebar:      
        #uploaded_files =  st.file_uploader("파일을 올려주세요.",type=['pdf','docx'],accept_multiple_files=True)
=========
    with st.sidebar:  
        uploaded_files =  st.file_uploader("파일을 올려주세요.",type=['pdf','docx'],accept_multiple_files=True)
>>>>>>>>> Temporary merge branch 2
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        process = st.button("Process")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)" 
        st.markdown("---")
        st.markdown(
            "## How to use\n"
            "1. OpenAI API key를 기입해주세요.\n"  
            "2. 채팅을 이용하여 법률 상담을 진행하세요.\n"
        ) 
        st.markdown("---")
        st.markdown("## About")
        st.markdown(
            "📖 챗봇을 통해 즉각적이고 정확한 답변을 얻을 수 있습니다."
        )

        # if "processComplete" not in st.session_state:
        #     st.session_state.processComplete = None
            
    if process:
        if not openai_api_key:
            st.info("OpenAI API key를 넣어주세요.")
            st.stop()
        #Retriever()
#            st.session_state.processComplete = True 

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    history = StreamlitChatMessageHistory(key="chat_messages")

    # 채팅 기록 삭제 
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    if user_input := st.chat_input("질문을 입력해주세요."):
        if not openai_api_key:
            st.info("OpenAI API key 를 입력하세요.")
            st.stop()
    
#       client = OpenAI(api_key=openai_api_key)

        category=get_retriever_category(user_input,openai_api_key)
        st.session_state.conversation = get_conversation_chain(Retriever.retrievers[category],openai_api_key) 
        
=========
        # 내 채팅 기록 남기기
>>>>>>>>> Temporary merge branch 2
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        st.chat_message("user").write(user_input)
        #       response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        # msg = response.choices[0].message.content
        # st.session_state.messages.append({"role": "assistant", "content": msg})
        # st.chat_message("assistant").write(msg)

        with st.chat_message("assistant"):
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):

                result = chain.invoke(user_input).content
                #with get_openai_callback() as cb:
=========
                result = chain.invoke(user_input)
                response_content = result.content
                st.write(response_content)
                # with get_openai_callback() as cb:
>>>>>>>>> Temporary merge branch 2
                    #st.session_state.chat_history = result['chat_history']
                #response = result['answer']                
        # AI 채팅 기록 남기기
        st.session_state.messages.append({"role": "assistant", "content": result.content})



if __name__ == '__main__':
    main()