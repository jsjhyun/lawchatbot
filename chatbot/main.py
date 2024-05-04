import chromadb
from openai import OpenAI
import streamlit as st
import tiktoken
from loguru import logger
# from retriever import rag_func
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from openai import OpenAI
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

def main():
    st.set_page_config(
    page_title="법률 상담 챗봇",
    page_icon=":books:")

    st.title("💬 법률 상담 챗봇")
    st.caption("쉽고, 편리한 법률 상담")

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
            "[OpenAI API key](https://platform.openai.com/account/api-keys)를 기입해주세요.\n"  
            "1. pdf, docx, txt 파일을 올려 사용할 수 있습니다.\n"
            "2. 채팅을 이용하여 법률 상담을 진행하세요.\n"
        ) 
        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖 챗봇을 사용하여 문서에 대해 질문하고 즉각적이고 정확한 답변을 얻을 수 있습니다. "
        )

        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #180C3D;
            }
        </style>
        """, unsafe_allow_html=True)

        # if "processComplete" not in st.session_state:
        #     st.session_state.processComplete = None
            
    if process:
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        files_text = get_text(uploaded_files)
        text_chunks = get_text_chunks(files_text)
        vetorestore = get_vectorstore(text_chunks)
        
        st.session_state.conversation = get_conversation_chain(vetorestore,openai_api_key) 

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

    if prompt := st.chat_input("질문을 입력해주세요."):
        if not openai_api_key:
            st.info("OpenAI API key 를 입력하세요.")
            st.stop()
    
#       client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        st.chat_message("user").write(prompt)
        #       response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        # msg = response.choices[0].message.content
        # st.session_state.messages.append({"role": "assistant", "content": msg})
        # st.chat_message("assistant").write(msg)

        with st.chat_message("assistant"):
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):
                result = chain({"question": prompt})
                with get_openai_callback() as cb:
                    st.session_state.chat_history = result['chat_history']
                response = result['answer']
                source_documents = result['source_documents']

                st.markdown(response)
                with st.expander("참고 문서 확인"):
                    st.markdown(source_documents[0].metadata['source'], help = source_documents[0].page_content)
                    st.markdown(source_documents[1].metadata['source'], help = source_documents[1].page_content)
                    st.markdown(source_documents[2].metadata['source'], help = source_documents[2].page_content)

# Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

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
        chunk_size=900,
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
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-3.5-turbo',temperature=0)
    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            chain_type="stuff", 
            retriever=vetorestore.as_retriever(search_type = 'mmr', vervose = True), 
            memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer'),
            get_chat_history=lambda h: h,
            return_source_documents=True,
            verbose = True
        )

    return conversation_chain


if __name__ == '__main__':
    main()