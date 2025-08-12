import fitz
import os

pdf_file_path = r'data\과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf'
doc = fitz.open(pdf_file_path) # 페이지별로 내용을 읽어논다

header_height =80 # 헤더(머리글) 높이 80으로 설정
footer_height =80  # 푸터(바닥글) 높이 80으로 설정
full_text = ''
# 문서 페이지 반복(각 페이지를 반복하여 텍스트 추출)
for page in doc:
    rect = page.rect # 페이지 크기 가져온다
    #print(rect)
    #print(rect.width) # 페이지 너비
    #print(rect.height) # 페이지 높이
    

    # 텍스트를 추출할 영역을 clip으로 지정
    header = page.get_text(clip=(0, 0, rect.width, header_height))
    # print(header)

    footer = page.get_text(clip=(0, rect.height-footer_height,rect.width,rect.height))

    text = page.get_text(clip =(0,header_height,rect.width, rect.height - footer_height))
    # 페이지 구분하기 위해 점선 추가
    full_text += text + '\n-------------------------------\n'
pdf_file_name = os.path.basename(pdf_file_path) # 파일명과 확장자 추출
# print(pdf_file_name)
pdf_file_name = os.path.splitext(pdf_file_name)[0] # 파일명만 추출
# output 풀더에 추출한 내용을 파일명.txt로 내보낸다
txt_file_path = f'output/{pdf_file_name}_with_preprocessing.txt'

with open(txt_file_path, 'w', encoding='utf-8') as f:
    # txt파일안에 추출한 모든 내용을 저장
    f.write(full_text)

