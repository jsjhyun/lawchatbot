from langchain_core.prompts import PromptTemplate
template = """법률 상담 챗봇입니다. 아래의 문제를 해결하기 위해선 어떤 절차가 필요할까요?
<사건>
{case}"""
prompt_template = PromptTemplate(
    template=template,
    input_variables=["case"],
)