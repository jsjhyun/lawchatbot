import streamlit as st

#IFRAME = '<iframe src="https://ghbtns.com/github-btn.html?user=IvanIsCoding&repo=ResuLLMe&type=star&count=true&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>'

st.markdown(
    f"""
    # 자주하는 질문 FAQ 
    """,
    unsafe_allow_html=True,
)

with st.expander("**OpenAI API Key가 꼭 필요한가요?**"):
    st.markdown(
    """
    **네!**, ChatGPT의 지원을 받습니다. [여기](https://platform.openai.com/account/api-keys)에서 키를 얻을 수 있습니다.
    """
    )

with st.expander("**질문을 작성해주세요~**"):
    st.markdown(
    """
    **답**
    """
    )

with st.expander("**여기도**"):
    st.markdown(
    """
    **답**
    """
    )

with st.expander("**질문**"):
    st.markdown(
    """
    **답**
    """
    )
