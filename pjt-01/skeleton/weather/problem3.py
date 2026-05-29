import requests
from pprint import pprint

# 문제3.
# 문제 2(B번)에서 얻은 결과를 활용하여
# 날씨 데이터의 KEY 값을 한글로 변경한 딕셔너리를 반환한다.
def get_result(api_key):
    # 1. OpenWeatherMap API 주소
    API_URL = 'https://api.openweathermap.org/data/2.5/weather'

    # 2. 요청 파라미터 설정
    params = {
        'q': 'Seoul,KR',   # 도시명, 국가 코드
        'appid': api_key  # 개인 API 키
    }

    # 3. API 요청 전송
    response = requests.get(API_URL, params=params)

    # 4. 응답 데이터를 JSON(dict) 형태로 변환
    parsed_data = response.json()

    # 5. main(기본 날씨 정보) 데이터 추출
    main_data = parsed_data['main']

    # 6. weather(날씨 상태 정보) 데이터 추출
    # weather는 리스트 형태이므로 첫 번째 요소 사용
    weather_data = parsed_data['weather'][0]

    # 7. 영문 KEY 값을 한글 KEY 값으로 변경하여 새로운 딕셔너리 구성
    result = {
        '온도': main_data['temp'],
        '체감온도': main_data['feels_like'],
        '최고온도': main_data['temp_max'],
        '최저온도': main_data['temp_min'],
        '습도': main_data['humidity'],
        '기압': main_data['pressure'],
        '요약': weather_data['description'],
        '아이콘': weather_data['icon'],
        '핵심': weather_data['main'],
        '식별자': weather_data['id']
    }

    # 8. 결과 반환
    return result


# 여러분의 OpenWeatherMap API 키를 설정하세요
api_key = 'b9c6e987ebd2b20bf844cecae3704cb0'

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_result(api_key)

    # pprint: 딕셔너리 데이터를 보기 좋게 출력
    pprint(result)
