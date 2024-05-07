from langchain_openai import ChatOpenAI
from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from retriever import *

class Search(BaseModel):
    """Search for information about 법."""

    query: str = Field(
        ...,
        description="Query to look up",
    )
    category: str = Field(
        ...,
        description="법 분류. Should be `형법` or `민법` or `헌법`.",
    )

def get_retriever_category(question, openai_api_key):
    system = """You have the ability to issue search queries to get information to help answer legal information."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=openai_api_key)
    structured_llm = llm.with_structured_output(Search)
    query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm
    return query_analyzer.invoke(question).category


class Retriever():
    criminal_pdf_url = "https://raw.githubusercontent.com/KwangWoonUnivCapstone/lawchatbot/main/chatbot/data/criminal_law.pdf"
    civil_law_pdf_url="https://raw.githubusercontent.com/KwangWoonUnivCapstone/lawchatbot/main/chatbot/data/civil_law.pdf"
    constitutionl_pdf_url="https://raw.githubusercontent.com/KwangWoonUnivCapstone/lawchatbot/main/chatbot/data/constitution.pdf"
    criminal_law_text = get_pdf(criminal_pdf_url)
    civil_law_text= get_pdf(civil_law_pdf_url)
    constitution_text = get_pdf(constitutionl_pdf_url)
    
    criminal_retriever = get_vectorstore(get_text_chunks(criminal_law_text)).as_retriever()
    civil_retriever = get_vectorstore(get_text_chunks(civil_law_text)).as_retriever()
    constitution_retriever = get_vectorstore(get_text_chunks(constitution_text)).as_retriever()
    retrievers = {
        "형법": criminal_retriever,
        "민법": civil_retriever,
        "헌법": constitution_retriever,
    }