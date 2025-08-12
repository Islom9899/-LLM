from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key) # OpenAI()로 클라이언트를 생성할 때 입력한 api_key적용

def get_ai_response(messages):
    """GPT에서 API로 답변을 받아오는 함수"""
    response = client.chat.completions.create(
        model='hpt-4o',
        temperature=0.9,
        messages=messages,# 대화 기록을 입력으로 전달
    
    )
    return response.choices[0].message.content
# 초기 시스탬 메스지 설정
messages = [
    {'role': 'system','content':'나는 사용자를 도와주는 상담사야.'}
]

while True:
    user_input = input('사용자 :')
    if user_input == 'exit':
        break

    messages.append({'role':'user','content':user_input}) # 사용자 메시지를 대화기록에 추가 
    ai_response = get_ai_response(messages) # 함수 호출하고 후 대화 기록 기반으로 AI 응답 가져오기
    messages.append({'role':'assistant','content':ai_response})
    print(f'Ai : {ai_response}')