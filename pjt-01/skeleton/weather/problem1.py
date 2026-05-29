import requests
from pprint import pprint

# 문제1. 날씨 데이터의 응답을 json 형태로 변환하여 key 값만 출력하시오.
def get_result(api_key):
    # 1. OpenWeatherMap API 주소
    API_URL = 'https://api.openweathermap.org/data/2.5/weather'

    # 2. 요청에 필요한 파라미터 설정
    params = {
        'q': 'Seoul,KR',   # 도시명, 국가 코드
        'appid': api_key  # 개인 API 키
    }

    # 3. API 요청 보내기
    response = requests.get(API_URL, params=params)

    # 4. 응답 데이터를 JSON 형태(dict)로 변환
    weather_data = response.json()

    # 5. JSON 데이터의 key 값들만 추출
    result = weather_data.keys()

    # 6. key 값 반환
    return result


# 여러분의 OpenWeatherMap API 키를 설정하세요
api_key = 'b9c6e987ebd2b20bf844cecae3704cb0'

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    result = get_result(api_key)
    # pprint: 딕셔너리 형태의 데이터를 보기 좋게 출력
    pprint(result)
