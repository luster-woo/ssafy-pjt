import pprint
import requests

# 전체 정기예금 상품 API 응답에서
# result 안에 포함된 key 값들만 출력하는 함수
def get_deposit_products():
    # 금융상품통합비교공시 API 인증키
    api_key = "f3f8b4d34b3c320a901179255b58ce3b"

    # 정기예금 상품 조회 API 엔드포인트
    API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    # 요청에 필요한 파라미터 설정
    # auth : API 인증키
    # topFinGrpNo : 금융권 코드 (020000 = 은행)
    # pageNo : 조회할 페이지 번호
    params = {
        "auth": api_key,
        "topFinGrpNo": "020000",
        "pageNo": 1
    }

    # 1️⃣ 정기예금 상품 조회 API 요청
    response = requests.get(API_URL, params=params)

    # 2️⃣ API 응답 데이터를 JSON 형식의 Python 딕셔너리로 변환
    deposit_data = response.json()

    # 3️⃣ 응답 데이터 중 실제 상품 정보가 담긴
    #     'result' 객체의 key 값들만 추출
    #     (예: baseList, optionList, err_cd, err_msg 등)
    result_keys = deposit_data["result"].keys()

    # result의 key 목록 반환
    return result_keys


# 아래 코드는 함수 동작 확인을 위한 실행 코드
if __name__ == '__main__':
    result = get_deposit_products()
    # pprint를 사용해 key 목록을 보기 좋게 출력
    pprint.pprint(result)
