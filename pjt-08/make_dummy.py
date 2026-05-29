import os
import django
import json

# 1. 기존 장고 프로젝트(pjt08)의 settings.py 환경을 그대로 가져와서 연결합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pjt08.settings')
django.setup()

from django.conf import settings
from openai import OpenAI

# 2. settings.py에 연결해둔 OPENAI_API_KEY를 안전하게 불러옵니다.
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 3. AI에게 내릴 페르소나 및 정교한 JSON 출력 프롬프트
prompt = """
당신은 대한민국 시중 은행의 15년 차 수석 상품 기획자입니다.
추천 알고리즘 학습에 사용할 가상의 정기예금 상품 데이터 10개를 JSON 형태로 생성해주세요.

[데이터 필수 조건]
1. 결측치나 타입 오류가 없어야 합니다.
2. 중복되는 데이터가 없어야 합니다.
3. 실제 시중 은행에서 판매할 법한 매력적이고 현실성 있는 데이터여야 합니다.

[JSON 키값 구조]
반드시 'dummy_data'라는 키 안에 리스트 형태로 아래 8개의 필드를 포함해야 합니다.
- fin_prdt_cd (상품코드, 예: DUMMY-001)
- kor_co_nm (은행명, 예: 우주은행)
- fin_prdt_nm (상품명, 예: 청년 도약 우대 정기예금)
- etc_note (상품 설명)
- join_deny (가입제한: 1, 2, 3 중 하나의 정수 값. 1:제한없음, 2:서민전용, 3:일부제한)
- join_member (가입대상)
- join_way (가입방법, 예: 스마트폰, 인터넷, 영업점)
- spcl_cnd (우대조건)
"""

print("🚀 생성형 AI가 더미 데이터를 기획하고 있습니다. 잠시만 기다려주세요...")

# 4. OpenAI API 호출 (반드시 JSON 형태로 달라고 강제합니다)
response = client.chat.completions.create(
    model="gpt-5-nano",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful data generator designed to output clean JSON."},
        {"role": "user", "content": prompt}
    ]
)

# 5. 결과 파싱
result_content = response.choices[0].message.content
dummy_data_json = json.loads(result_content)

# 6. dummy_data.json 파일로 저장
file_path = os.path.join(settings.BASE_DIR, 'dummy_data.json')

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(dummy_data_json['dummy_data'], f, ensure_ascii=False, indent=4)

print(f"🎉 성공! {file_path} 파일이 완벽하게 생성되었습니다.")