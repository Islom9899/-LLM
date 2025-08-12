from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

# 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant.'),
    ('user', '{input}'),
])

# 문자열 출력 파서 
output_parser = StrOutputParser()


# 체인 구성
chain = prompt | llm | output_parser

result = chain.invoke({'input':'hi'})
print(result)

result2 = chain.stream({'input':'K-pop'})
for token in result2:
    print(token, end='', flush=True)
