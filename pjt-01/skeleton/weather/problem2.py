import requests
from pprint import pprint

# 문제2.
# 날씨 데이터 중 KEY 값이 "main", "weather" 인 데이터만
# 새로운 딕셔너리에 담아 반환하는 함수
def get_result(api_key):
    # 1. OpenWeatherMap API 주소
    API_URL = 'https://api.openweathermap.org/data/2.5/weather'

    # 2. 요청 파라미터 설정
    params = {
        'q': 'Seoul,KR',   # 도시명과 국가 코드
        'appid': api_key  # 개인 API 키
    }

    # 3. API 요청 보내기
    response = requests.get(API_URL, params=params)

    # 4. 응답 데이터를 JSON(dict) 형태로 변환
    weather_data = response.json()

    # 5. 필요한 데이터(main, weather)만 추출하여 새로운 딕셔너리 구성
    result = {
        'main': weather_data['main'],
        'weather': weather_data['weather']
    }

    # 6. 결과 반환
    return result


# 여러분의 OpenWeatherMap API 키를 설정하세요
api_key = 'b9c6e987ebd2b20bf844cecae3704cb0'

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_result(api_key)

    # pprint: 딕셔너리 데이터를 보기 좋게 출력
    pprint(result)
