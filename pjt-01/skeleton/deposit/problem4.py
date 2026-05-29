import pprint
import requests

# 정기예금 상품 정보(baseList)와
# 금리 및 가입 조건 정보(optionList)를
# 금융상품 코드(fin_prdt_cd)를 기준으로 매칭하여
# 하나의 구조화된 객체로 반환하는 함수
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

    # 2️⃣ 응답 데이터를 JSON 형식의 Python 딕셔너리로 변환
    data = response.json()

    # 실제 상품 정보가 담긴 result 객체 추출
    result = data['result']

    # 3️⃣ 정기예금 상품의 기본 정보 목록
    #     (금융회사명, 상품명, 금융상품 코드 등)
    base_list = result['baseList']

    # 4️⃣ 정기예금 상품의 옵션 정보 목록
    #     (금리, 저축기간, 금리유형 등)
    option_list = result['optionList']

    # 최종 결과를 담을 리스트
    final_result = []

    # 5️⃣ baseList를 기준으로 순회하며
    #     optionList에서 같은 금융상품 코드를 가진
    #     모든 옵션 정보를 매칭
    for base in base_list:
        # 현재 상품의 금융상품 코드
        product_code = base['fin_prdt_cd']

        # 해당 상품의 금리 옵션 정보를 담을 리스트
        option_info_list = []

        # 모든 옵션 리스트를 순회하며
        # 상품 코드가 같은 옵션만 추출
        for option in option_list:
            if option['fin_prdt_cd'] == product_code:
                option_info = {
                    # 기본 저축 금리
                    '저축금리': option['intr_rate'],

                    # 최고 우대 금리
                    '최고우대금리': option['intr_rate2'],

                    # 저축 기간 (개월 단위)
                    '저축기간': option['save_trm'],

                    # 저축 금리 유형 코드
                    '저축금리유형': option['intr_rate_type'],

                    # 저축 금리 유형명 (단리/복리 등)
                    '저축금리유형명': option['intr_rate_type_nm']
                }

                # 해당 상품의 옵션 리스트에 추가
                option_info_list.append(option_info)

        # 상품 기본 정보 + 옵션 정보를 하나의 딕셔너리로 구성
        product_dict = {
            '금융상품명': base['fin_prdt_nm'],
            '금융회사명': base['kor_co_nm'],
            '금리정보': option_info_list
        }

        # 6️⃣ 가공된 상품 정보를 최종 결과 리스트에 추가
        final_result.append(product_dict)

    # 모든 정기예금 상품 + 옵션 정보 반환
    return final_result


# 아래 코드는 함수가 정상 동작하는지 확인하기 위한 실행 코드
if __name__ == '__main__':
    result = get_deposit_products()
    # pprint를 사용해 중첩된 구조를 보기 좋게 출력
    pprint.pprint(result)
