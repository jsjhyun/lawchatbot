from openai import OpenAI
import streamlit as st

def main():
    st.set_page_config(
    page_title="chatbot",
    page_icon=":books:")

    st.title("💬 법률 상담 챗봇")
    st.caption("A streamlit chatbot powered by OpenAI LLM")

    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"    

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 고민이 있으면 언제든 물어봐주세요!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat Logic
    if prompt := st.chat_input("고민 있는 법률 문제를 입력해주세요!"):
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})

        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if __name__ == '__main__':
    main()