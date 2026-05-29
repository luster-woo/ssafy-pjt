## - 기술적 난관 및 해결 과정 (학습 내용)

프로젝트 진행 중 발생했던 주요 문제들과 해결 과정입니다.

1. **Proxy 서버와 API 경로 충돌 문제 (404 오류):**
   * **현상:** 프론트엔드 fetch 요청 시 `/api/v1/` 경로와 app 내부 URL 경로가 중복되어 `404 Not Found` 오류가 반복적으로 발생함.
   * **해결:** Django의 `urls.py` 구조를 재정리하여 메인 URL과 app URL의 역할을 분리함. 프론트엔드 fetch 주소도 실제 라우팅 구조에 맞게 통일하여 해결함.

2. **Serializer 필드 불일치 문제 (`KeyError`, `Bad Request`):**
   * **현상:** 프론트엔드에서 전달한 JSON 형식과 DRF Serializer의 필드명이 달라 `prompt required`, `undefined`, `KeyError: 'url'` 등의 오류가 발생함.
   * **해결:** Request/Response Serializer의 필드명을 services.py의 반환값과 동일하게 맞추고, 프론트엔드 요청 body 구조를 통일하여 데이터 흐름을 일관성 있게 수정함.

3. **GMS API 응답 파싱 오류 (`choices`, `data` KeyError):**
   * **현상:** GMS API 호출 실패 시 응답 JSON에 `choices` 또는 `data` 키가 존재하지 않아 서버 내부 오류(500)가 발생함.
   * **해결:** API 응답 전에 `print(data)`로 실제 응답을 확인하고, 키 존재 여부를 검사하는 예외 처리 로직을 추가함. 실패 시 기본 이미지 및 기본 응답을 반환하도록 fallback 로직을 구현함.

4. **이미지 생성 모델 호출 문제:**
   * **현상:** 텍스트 모델과 이미지 모델 호출 구조가 혼합되어 이미지 생성 API 호출 시 오류가 발생함.
   * **해결:** 이미지 생성 전용 API 엔드포인트를 별도로 구성하고, `gpt-image-1` 모델을 사용하는 이미지 전용 service 함수로 분리하여 처리함.

5. **CORS 및 프론트엔드 통신 문제:**
   * **현상:** HTML fetch 요청 시 브라우저에서 CORS 오류가 발생하여 API 통신이 차단됨.
   * **해결:** `django-cors-headers`를 설치하고 `settings.py`에 middleware 및 `CORS_ALLOW_ALL_ORIGINS=True` 설정을 추가하여 해결함.

---

## -. 느낀 점

* **API 구조 설계의 중요성:**  
  Proxy 서버를 중심으로 FastAPI, Django, 프론트엔드가 연결되는 구조를 구현하며 단순 기능 구현보다 API 경로와 데이터 형식을 일관성 있게 설계하는 것이 매우 중요하다는 점을 배움.

* **디버깅 경험 향상:**  
  401, 404, 500, KeyError 등 다양한 오류를 직접 해결하며 서버 로그 분석과 request/response 구조 확인 능력이 향상됨.

* **Serializer와 데이터 검증의 중요성:**  
  DRF Serializer를 통해 프론트엔드와 백엔드 간 데이터 형식을 강하게 제한하면 안정적인 API 구현이 가능하다는 점을 체감함.

* **사용자 경험(UI/UX)의 중요성:**  
  로딩 애니메이션, 상태 메시지, 가드레일 결과 출력 등을 구현하며 사용자가 시스템 상태를 직관적으로 이해할 수 있도록 만드는 과정이 중요하다고 느낌.

* **생성형 AI 서비스 구조 이해:**  
  GMS API와 Proxy 서버를 연결하며 실제 AI 서비스가 어떤 방식으로 요청을 중계하고 응답을 처리하는지 구조적으로 이해할 수 있었음.