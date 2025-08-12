# 도시별 시간 알려주기 - 문자열 형식으로 받은 타임존을 시각구하기
# ex) 서울-> 오후 8시 20시

from datetime import datetime
import pytz

def get_current_time(timezone: str='Asia/Seoul'):
    """GPT가 현재 시간을 파악할 수 있게 해주는 함수 - 현재 시간 출력/반환"""
    tz = pytz.timezone(timezone) # 타임존 설정
    # 타임존에 맞는 현재 시간 -> 형식에 맞춘다 -> now변수에 담는다
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone

tools = [
    {
        'type':'function',
        'function':{
            'name':'get_current_time',
            'discription':'해당 타임존의 날짜와 시간을 반환합니다.',
            'parameters':{
                'type':'object',
                'properties':{
                    'timezone':{
                        'type':'string',
                        'discription':'현재 날짜와 시간을 반환할 타임존을 입력하세요.(예: Asia/Seoul)',
                    },
                    
                },
                'required':['timezone'],
            },
        },
    }
]
if __name__ == '__main__':
    get_current_time('America/New_York')

print(__name__)  # 위지