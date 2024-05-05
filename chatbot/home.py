from openai import OpenAI
import streamlit as st

def main():
    st.set_page_config(
    page_title="법률 상담 챗봇",
    page_icon=":books:")

    st.title("💬 법률 상담 챗봇")
    st.caption("쉽고, 편리한 법률 상담")

    with st.sidebar:
        
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
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
            "📖 챗봇을 사용하여 문서에 대해 질문하면 즉각적이고 정확한 답변을 얻을 수 있습니다. "
        )

        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #180C3D;
            }
        </style>
        """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 채팅 기록 삭제 
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)    

    if prompt := st.chat_input("질문을 입력해주세요."):
        if not openai_api_key:
            st.info("OpenAI API key 를 입력해주세요.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if __name__ == '__main__':
    main()