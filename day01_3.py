from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key) # OpenAI()로 클라이언트를 생성할 때 입력한 api_key적용

response = client.chat.completions.create(
    model='gpt-4o', # model은 어떤 언어 모델을 사용할지 정하는 부분
    temperature=0.9, # 문장을 생성할 때 무작위성을 조절
    messages=[ # GPT가 과거의 대화를 기반으로 적절한 응답을 생성하는 데 필요한 매개변수
        {'role':'system', 'content':'너는 백설공주 이야기 속의 거울이야. 그 이야기 속의 마법 거울의 캐릭터에 부합하게 답변해줘.'}, 
        {'role':'user', 'content':'세상에서 누가 제일 아름답니?'},
    ]
)

print(response) # 사용한 토큰 수나 언어 모델의 역할 등 여러 정보가 담겨있다

print('-' * 10)
print(response.choices[0].message.content) # 답변 내용만 출력

