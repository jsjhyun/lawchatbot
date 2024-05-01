from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings

loader = DirectoryLoader('/content/TS_1.판결문/1.Training/원천데이터/TS_1.판결문/02.형사/2020')
docs = loader.load()

model_name = "jhgan/ko-sroberta-multitask" #KorNLU 데이터셋에 학습시킨 한국어 임베딩 모델
model_kwargs = {'device' : 'cpu'}
encode_kwargs = {'normalize_embeddings' : False}
embedding_model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
#prompt = hub.pull("rlm/rag-prompt")

from langchain_core.prompts import PromptTemplate

template = """아래 내용을 바탕으로 법률 상담을 도와주어야해. 질문에 대한 답을 구체적으로 해.
{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    #| StrOutputParser()
)

rag_chain.invoke("음주운전 2회로 집행유예 기간 중, 무면허 음주운전으로 적발되었습니다.저는 업무상 차량이 필수적인 직업을 가지고 있어, 면허 취소 이후에도 집행유예 기간동안 타인의 명의로 몰래 차량을 이용해왔습니다. 최근 다시 음주운전을 하게 되었고, 그러던 중 차 안에서 잠이 들어 경찰에 적발되었습니다. 저는 술을 마시고 약 7시간 뒤에 적발되었고, 측정 결과 혈중알코올농도는 0.083이었습니다. 부모님께도 죄송하고,특히 자력으로는 생활할 수 없는 가족을 돌봐야 하는 상황에서 실형을 피할 수 있는 방법과 면허를 구제받을 수 있는 방법이 있는지 알고 싶습니다.")