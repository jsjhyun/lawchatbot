import streamlit as st
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from retriever import *
from multiple_retriever import *

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
        st.markdown(
            "## Please Check!\n"
            "1. [변호사법 109조]\n'변호사가 아닌자'의 유상 법률 상담 및 법률 문서 작성을 금지한다.\n"  
            "2. 결정에 대한 책임은 사용자에게 있음을 고지한다.\n"
        ) 
        st.markdown("---")
        st.markdown("## About")
        st.markdown(
            "📖 챗봇을 통해 즉각적이고 정확한 답변을 얻을 수 있습니다."
        )

    if process:
        if not openai_api_key:
            st.info("OpenAI API key를 넣어주세요.")
            st.stop()

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
    
        category=get_retriever_category(user_input,openai_api_key)
        st.session_state.conversation = get_conversation_chain(Retriever.retrievers[category],openai_api_key) 
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):

                result = chain.invoke(user_input).content
                result = chain.invoke(user_input)
                response_content = result.content
                st.write(response_content)
           
        # AI 채팅 기록 남기기
        st.session_state.messages.append({"role": "assistant", "content": result.content})

if __name__ == '__main__':
    main()
