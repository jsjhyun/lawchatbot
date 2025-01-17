import streamlit as st

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

with st.expander("**어떻게 법률 정보를 얻나요?**"):
    st.markdown(
    """
    법제체 국가법령정보센터의 공공데이터를 학습했습니다.
    """
    )

with st.expander("**어떤 식으로 질문을 해야할까요? 요령을 알려주세요!**"):
    st.markdown(
    """
    현재 처한 상황을 적으시고 만약 관련 법률도 출력하길 원하신다면 질문하실 때 "관련 법률을 근거로 들어서 설명해줘"라고 질문해주세요.
    """
    )

with st.expander("**주의 할 점이 있나요?**"):
    st.markdown(
    """
    챗봇에서 생성된 내용이 부정확하거나 실상황과 다른 내용을 출력할 수 있으니 자세한 상담은 법조인에게 물어보는 것을 권장합니다.
    """
    )
