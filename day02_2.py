import fitz
import os

pdf_file_path = r'data\과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf'
doc = fitz.open(pdf_file_path) # 페이지별로 내용을 읽어논다

full_text = ''
# 문서 페이지 반복(각 페이지를 반복하여 텍스트 추출)
for page in doc:
    text = page.get_text() # 페이지의 텍스트 추출
    # full_text 라는 비어있는 변수에 한 페이지씩 추가
    full_text += text

    pdf_file_name = os.path.basename(pdf_file_path) # 파일명과 확장자 추출
    # print(pdf_file_name)
    pdf_file_name = os.path.splitext(pdf_file_name)[0] # 파일명만 추출
    # output 풀더에 추출한 내용을 파일명.txt로 내보낸다
    txt_file_path = f'output/{pdf_file_name}.txt'

    with open(txt_file_path, 'w', encoding='utf-8') as f:
        # txt파일안에 추출한 모든 내용을 저장
        f.write(full_text)
        
