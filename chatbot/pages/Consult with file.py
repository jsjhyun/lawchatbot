import streamlit as st
import tiktoken
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.runnables import RunnablePassthrough
from prompt import get_prompt_pdf

def main():
    st.set_page_config(
    page_title="law chat",
    page_icon=":books:")

    st.title("💬 법률 문서 분석")
    st.caption("쉽고, 편리한 문서 요약")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    with st.sidebar:      
        uploaded_files =  st.file_uploader("파일을 올려주세요.",type=['pdf','docx'],accept_multiple_files=True)
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        process = st.button("Process")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)" 
        st.markdown("---")
        st.markdown(
            "## How to use\n"
            "1. OpenAI API key를 기입해주세요.\n"  
            "2. pdf, docx, txt 파일을 올려 법률 문서를 분석하도록 합니다.\n"
            "3. 채팅을 이용하여 법률 문서에 관한 상담을 진행하세요.\n"
            "* Open Api Key, file 모두 넣어야 진행이 가능합니다."
        ) 
        st.markdown("---")
        st.markdown(
            "## Please Check!\n"
            "1. [변호사법 109조]\n'변호사가 아닌자'의 유상 법률 상담 및 법률 문서 작성을 금지한다.\n"  
            "2. 결정에 대한 책임은 사용자에게 있음을 고지한다.\n"
        ) 
        st.markdown("---")
        st.markdown("## About")
        st.markdown(
            "📖 챗봇을 통해 즉각적이고 정확한 답변을 얻을 수 있습니다. "
        )

    if process:
        if not uploaded_files:
            st.warning('파일을 올려주세요.')
            if not openai_api_key:
                st.warning("OpenAI API key를 넣어주세요.")
            st.stop()

        if not openai_api_key:
            st.warning("OpenAI API key를 넣어주세요.")
            st.stop()
        files_text = get_text(uploaded_files)
        text_chunks = get_text_chunks(files_text)
        vetorestore = get_vectorstore(text_chunks)
        
        st.session_state.conversation = get_conversation_chain(vetorestore,openai_api_key) 

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 문서를 요약 & 분석해 드립니다!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    history = StreamlitChatMessageHistory(key="chat_messages")

    # 채팅 기록 삭제 
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 법률 문서를 요약 & 분석해 드립니다!"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    if user_input := st.chat_input("질문을 입력해주세요."):
        if not openai_api_key:
            st.info("OpenAI API key 를 입력해주세요.")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": user_input})      
        st.chat_message("user").write(user_input)
        
        with st.chat_message("assistant"):
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):
                result = chain.invoke(user_input)
                response_content = result.content
                st.write(response_content)

        # AI 채팅 기록 남기기
        st.session_state.messages.append({"role": "assistant", "content": result.content})

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)

def get_text(docs):

    doc_list = []
    
    for doc in docs:
        file_name = doc.name  # doc 객체의 이름을 파일 이름으로 사용
        with open(file_name, "wb") as file:  # 파일을 doc.name으로 저장
            file.write(doc.getvalue())
            logger.info(f"Uploaded {file_name}")
        if '.pdf' in doc.name:
            loader = PyPDFLoader(file_name)
            documents = loader.load_and_split()
        elif '.docx' in doc.name:
            loader = Docx2txtLoader(file_name)
            documents = loader.load_and_split()
        elif '.pptx' in doc.name:
            loader = UnstructuredPowerPointLoader(file_name)
            documents = loader.load_and_split()

        doc_list.extend(documents)
    return doc_list

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=tiktoken_len
    )
    chunks = text_splitter.split_documents(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
                                        model_name="jhgan/ko-sroberta-multitask",
                                        model_kwargs={'device': 'cpu'},
                                        encode_kwargs={'normalize_embeddings': True}
                                        )  
    
    vectordb = FAISS.from_documents(text_chunks, embeddings)
    return vectordb

def get_conversation_chain(vetorestore,openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-4',temperature=0)
    conversation_chain = (
        {"context": vetorestore.as_retriever() , "question": RunnablePassthrough()}
        | get_prompt_pdf()
        | llm
        )
    return conversation_chain

if __name__ == '__main__':
    main()
