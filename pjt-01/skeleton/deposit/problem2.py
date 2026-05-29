import pprint
import requests

# 전체 정기예금 상품의 기본 정보 리스트(baseList)를 반환하는 함수
def get_deposit_products():
    # 금융상품통합비교공시 API 인증키
    api_key = "f3f8b4d34b3c320a901179255b58ce3b"

    # 정기예금 상품 조회 API 엔드포인트
    API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    # API 요청 시 전달할 파라미터
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

    # 2️⃣ 응답 데이터를 JSON 형식의 Python 딕셔너리로 변환
    deposit_data = response.json()

    # 3️⃣ 응답 데이터 중 실제 정기예금 상품의 기본 정보가 담긴
    #     result → baseList 데이터 추출
    #     (금융회사명, 상품명, 금융상품 코드 등 포함)
    base_list = deposit_data["result"]["baseList"]

    # 정기예금 상품 기본 정보 리스트 반환
    return base_list


# 아래 코드는 함수가 정상 동작하는지 확인하기 위한 실행 코드
if __name__ == '__main__':
    result = get_deposit_products()
    # pprint를 사용해 리스트 형태의 데이터를 보기 좋게 출력
    pprint.pprint(result)
