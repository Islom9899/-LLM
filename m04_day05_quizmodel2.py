# 라이브러리
from glob import glob
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def encode_image(image_path):
    """이미지 파일을 읽어 base64 문자열로 변환하는 함수"""
    with open(image_path,'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_quiz(image_path, n_trial=0, max_trial=3):
    """이미지 경로를 받아 퀴지를 만드는 함수"""
    if n_trial >=max_trial: # 최대 문제 생성 횟수를 넘어서면 강제로 예외 발생
        raise Exception('Failed to generate a quiz.')
    
    # base64로 이미지를 인코딩
    base64_image = encode_image(image_path)

    # quiz_primpt
    quiz_prompt = """
    제공된 이미지를 바탕으로, 다음과 같은 양식으로 퀴즈를 만들어주세요. 
    정답은 1~4 중 하나만 해당하도록 출제하세요.
    토익 리스닝 문제 스타일로 문제를 만들어주세요.
    아래는 예시입니다. 
    ----- 예시 -----

    Q: 다음 이미지에 대한 설명 중 옳지 않은 것은 무엇인가요?
    - (1) 베이커리에서 사람들이 빵을 사고 있는 모습이 담겨 있습니다.
    - (2) 맨 앞에 서 있는 사람은 빨간색 셔츠를 입고 있습니다.
    - (3) 기차를 타기 위해 줄을 서 있는 사람들이 있습니다.
    - (4) 점원은 노란색 티셔츠를 입고 있습니다.

    Listening: Which of the following descriptions of the image is incorrect?
    - (1) It shows people buying bread at a bakery.
    - (2) The person standing at the front is wearing a red shirt.
    - (3) There are people lining up to take a train.
    - (4) The clerk is wearing a yellow T-shirt.
        
    정답: (4) 점원은 노란색 티셔츠가 아닌 파란색 티셔츠를 입고 있습니다.
    (주의: 정답은 1~4 중 하나만 선택되도록 출제하세요.)
    ======
    """
    messages = [
        {
            'role':'user',
            'content':[
                {'type':'text', 'text':quiz_prompt},
                {
                    'type':'image_url',
                    'image_url': {'url':f'data:image/jpeg;base64, {base64_image}'},
                },
            ],
        }
    ]
    # try ~ except -> 예외 처리 구문
    try: # 정상적이면 gpt모델을  이용해서 응답받는다
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages
        )
    except Exception as e: # 예외(오류)가 발생하면 image_quiz함수 호출
        print(f'failed\n + {str(e)}')
        return image_quiz(image_path, n_trial+1) # 재귀 함수 호줄
    
    content = response.choices[0].message.content # 응답 결과를 content 변수에 저장

    if 'Listening:' in content: # 여어 구문이 있는가? -> 영어 듣기 문제를 민들수 있다
        return content, True
    else: # 영어 구문이 없다 -> 영어 듣기 문재를 만들수 없다 -> 함수 호출해서 gpt모델이 호출 생성하도록
        return image_quiz(image_path,n_trial+1)

# ------------------------------------------------------------
# 여러 문제를 불러오기 의한 코드
# 마크다운 파일 생성 -> .md
# TTC (글자 -> 말) 인식을 위해서 json파일 생성 -> .json

# 문제들을 계속 붙여 나가기 위해서 빈 문자열 선언
txt = ''
eng_dict = [] # 영어 문제만 담기 위해 생성
no =1 # 문제 번호를 1로 초기화

# images풀더 내의 모든 jpg파일을 사용
for g in glob('./images/*.jpg'):
    q, is_suceed = image_quiz(g) # g -> 이미지 객체 1개

    # 문제 생성에 실패하면 다음 문제로 넘어간다
    if not is_suceed:
        continue # 다음 이미지로 넘어간다(아래 코드는 실행되지 않는다)

    divider = f'## 문제 {no}\n\n'
    print(divider)

    txt += divider
    # 파일명 추출해서 이미지 링크 만들기
    filename = os.path.basename(g) # 마크다운에 표시할 이미지파일 경로 설정
    txt += f'![image]({filename})\n\n'

    # 문제 추가
    print(q)
    # txt 문자열 변수에 마크다운 코드가 계속 추가된다
    txt += f'{q}\n\n------------------------------\n\n'
    
    # 마크다운 파일로 저장
    with open('./images/image_quiz_eng.md', 'w', encoding='utf-8') as f:
        f.write(txt)
        # 영어 문제만 추출
        # .split() -> 괄호 안 내용 기준 분리 -> 결과가 리스트형태
        # .strip() -> 공백 앞뒤로 제거
    eng = q.split('Listening: ')[1].split('정답: ')[0].strip()

    eng_dict.append({
        'no' : no,
        'eng' : eng,
        'img' : filename
    })

    # json파일로 저장
    with open('image_quiz_eng.json','w', encoding='utf-8') as f:
        json.dump(eng_dict, f, ensure_ascii=False,indent=4)

    no +=1
