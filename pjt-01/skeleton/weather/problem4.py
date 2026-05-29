import requests
from pprint import pprint

# 문제4.
# 문제 3(C번)에서 얻은 데이터를 활용하여
# 켈빈(K) 온도 값 아래에 섭씨(℃) 온도 데이터를 추가한다.
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
    data = response.json()

    # 5. 기본 날씨 정보(main)와 날씨 상태(weather) 데이터 추출
    main = data['main']
    weather = data['weather'][0]  # weather는 리스트이므로 첫 번째 요소 사용

    # 6. 켈빈(K) → 섭씨(℃) 변환 함수 정의
    def k_to_c(k):
        return round(k - 273.15, 2)

    # 7. 기존 온도 데이터 아래에 섭씨 데이터를 추가하여 결과 구성
    result = {
        '기본': {
            # 해수면 기압(sea_level)은 없을 수도 있으므로 get 사용
            None: main.get('sea_level'),

            '기압': main['pressure'],
            '습도': main['humidity'],

            '온도': main['temp'],
            '온도(섭씨)': k_to_c(main['temp']),

            '체감온도': main['feels_like'],
            '체감온도(섭씨)': k_to_c(main['feels_like']),

            '최고온도': main['temp_max'],
            '최고온도(섭씨)': k_to_c(main['temp_max']),

            '최저온도': main['temp_min'],
            '최저온도(섭씨)': k_to_c(main['temp_min']),
        },

        '날씨': [
            {
                '식별자': weather['id'],
                '아이콘': weather['icon'],
                '요약': weather['description'],
                '핵심': weather['main']
            }
        ]
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
