from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 평가를 위한 프롬프트 템플릿 정의
prompt_template = " 이 음식 리뷰 '{review}'에 대해  '{rating1}'점부터 '{rating2}'점까지의 평가를 해주세요."
prompt = PromptTemplate(
    input_variables=['review','rating1','rating2'], template=prompt_template
)

# 모델 -> gpt -3.5-turbo
openai = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)

chain = prompt | openai | StrOutputParser()

# 사용자의 리뷰와 점수 범위 입력 -> AI 모델에게 평가를 용청
# 오류가 발생할 경우  예외 처리
# 사용자의 리뷰에 대한 평가를 요청한다.
try:
    with open('review_result_1.txt','w', encoding='utf-8') as f:
        response = chain.invoke({
            "review": "맛은 있엇지만 배달 포장이 부족하여서 아쉬웠습니다.",
            "rating1": "1",
            "rating2": "5"
    })
        f.write(f"평가 결과: {response}\n")
    print('평가 결과가 review_reult_1.txt 파일에 저장되었습니다!')
except Exception as e:
    print(f"Error: {e}")

print('-' * 50)

with open('review_result_2.txt','w', encoding='utf-8') as f:
    response2  = chain.stream({
    'review': '맛은 있었지민 배달 포장 상태가 아쉬웠습니다.',
    'rating1':'1',
    'rating2':'5',
})
    for token in response2:
        f.write(token)
        print(token, end='',flush=True)



