# PDF 로드
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader('unsu.pdf')
pages = loader.load_and_split()

# print(pages[0])

# 텍스트 분할하기
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.split_documents(pages)
# print(texts[0])

# 임베딩
embeddings_model = OpenAIEmbeddings(
    model = 'text-embedding-3-large',
)

# 벡터 DB
db = Chroma.from_documents(texts, embeddings_model)

# 검색기
question = '아내가 먹고 싶어하는 음식은 무엇이야?'
llm = ChatOpenAI(temperature=0)
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(),llm=llm
)
#   docs = retriever_from_llm.invoke(question)
#  print(len(docs))
#   print(docs)

# 프롬프트 템플릿
prompt = hub.pull('rlm/rag-prompt')

# 사용자 함수 정의 - 결과 포맷을 예쁘게 해주는 목적의 함수(page_content)
def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

# 체인
rag_chain = (
    {'context': retriever_from_llm | format_docs,
     'question':RunnablePassthrough()}
     | prompt
     | llm
     | StrOutputParser()
)

# 질문
result = rag_chain.invoke('아내가 먹고 싶어하는 음식이 무엇이야?')
print(result)