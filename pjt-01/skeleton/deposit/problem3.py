import pprint
import requests

# 정기예금 상품들의 옵션(optionList) 정보 중
# 필요한 항목만 추출하여 새로운 리스트로 반환하는 함수
def get_deposit_products():
    # 금융상품통합비교공시 API 인증키
    api_key = "f3f8b4d34b3c320a901179255b58ce3b"

    # 정기예금 상품 조회 API 엔드포인트
    API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    # API 요청 파라미터 설정
    # auth : API 인증키
    # topFinGrpNo : 금융권 코드 (020000 = 은행)
    # pageNo : 조회 페이지 번호
    params = {
        "auth": api_key,
        "topFinGrpNo": "020000",
        "pageNo": 1
    }

    # 1️⃣ 정기예금 상품 조회 API 요청
    response = requests.get(API_URL, params=params)

    # 2️⃣ API 응답 데이터를 JSON 형식의 Python 딕셔너리로 변환
    deposit_data = response.json()

    # 3️⃣ 응답 데이터 중
    #     정기예금 상품의 금리 및 가입 조건 정보가 담긴
    #     result → optionList 저장
    option_list = deposit_data["result"]["optionList"]

    # 4️⃣ optionList를 순회하며
    #     필요한 정보만 추출해 새로운 리스트로 가공
    result = []

    for option in option_list:
        temp = {
            # 금융회사 고유 코드
            "금융회사코드": option["fin_co_no"],

            # 금융상품 코드 (baseList와 매칭할 때 사용)
            "상품코드": option["fin_prdt_cd"],

            # 금리 유형 (단리/복리 등)
            "금리유형": option["intr_rate_type_nm"],

            # 저축 기간 (개월 단위)
            "저축기간": option["save_trm"],

            # 기본 금리
            "기본금리": option["intr_rate"],

            # 최고 우대 금리
            "최고금리": option["intr_rate2"]
        }

        # 가공된 옵션 정보를 결과 리스트에 추가
        result.append(temp)

    # 가공된 정기예금 옵션 리스트 반환
    return result


# 아래 코드는 함수 동작 확인을 위한 실행 코드
if __name__ == '__main__':
    result = get_deposit_products()
    # pprint를 사용해 리스트 형태의 데이터를 보기 좋게 출력
    pprint.pprint(result)
