# gpt_functions.py 파일의 get_current_time 함수와 tools를 임포트한다.
from gpt_functions import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
# GPT가 json형태의 문자열을 반환할 때 읽기 위한 라이브러리 임포
import json 
import streamlit as st

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_ai_response(messages, tools=None):
    """tools에 gpt_functions의 tools를 대입해주면 get_current_time 함수를 사용할 수 있다."""
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        tools=tools,
    )
    return response
# -------------------------------------------------------------------------------
# 스트림릿 부분
st.title('💬 Chatbot')  # 스트림릿 웹 페이지 상단에 제목이 나오도록

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role':'system',
         'content':'너는 사용자를 도와주는 이슬럼님 만든 상담사야.'
        }, # 초기 시스템 메세지
    ]
for msg in st.session_state.messages:
    if msg['role'] == 'assistant' or msg['role'] == 'user':
        st.chat_message(msg['role']).write(msg['content'])

if user_input := st.chat_input():
    st.session_state.messages.append(
        {
            'role' : 'user',
            'content' : user_input
        }
    )
    st.chat_message('user').write(user_input)

    #-------------------------------------------------------------------
    ai_response = get_ai_response(st.session_state.messages, tools=tools) # 함수 호출 -> 객체 형태로 반환
    ai_message = ai_response.choices[0].message
    print(ai_message) # ai_message의 값이 어떤 형태인지 임시 출력
    # GPT가 특정 함수를 실행해야 한다고 판단하면 ai_message의 tool_calls라는 속성에
    # 실행할 함수의 정보가 포함된다.
    # --> tool_calls가 있다면 함수를 실행해야 한다고 GPT가 판단했다는 뜻이다.
    tool_calls = ai_message.tool_calls
    if tool_calls: # tool_calls가 있는 경우
        for tool_call in tool_calls:
            tool_name = tool_call.function.name  # 실행할 함수명
            tool_call_id = tool_call.id  # 펑션 콜링의 id
            
            # get_current_time함수를 실행할 때 타임존 정보가 필요하므로
            # 필요한 값을 arguments에 추가한다.
            # --> GPT가 반환한 json형태의 문자열을 딕셔너리로 바꿔야 한다.
            arguments = json.loads(tool_call.function.arguments)
            
            if tool_name == 'get_current_time':
                st.session_state.messages.append(
                    {
                    'role':'function', # role을 'function'으로 설정
                    'tool_call_id': tool_call_id,
                    'name': tool_name,
                    'content': get_current_time(timezone=arguments['timezone']), # 함수 실행 결과를 content로 설정
                    }
                )
        st.session_state.messages.append({
            'role':'system',
            'content':'이제 주어진 결과를 바탕으로 답변할 차례다.'
        })
        
        # get_ai_response 함수를 다시 한번 호출하여 GPT의 답을 받는다.
        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message
    
    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content':ai_message.content
        }
    )
    print('AI\t: ' + ai_message.content)
    st.chat_message('assistant').write(ai_message.content)