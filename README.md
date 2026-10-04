# 🏫 SSAFY 15기 관통 프로젝트

[![SSAFY](https://img.shields.io/badge/SSAFY-15기%20구미-blue?style=flat-square)](https://www.ssafy.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/ko/docs/Web/JavaScript)

SSAFY 15기 과정에서 진행한 관통 프로젝트 기록입니다.  
Python 기초부터 시작해 데이터 분석, Django 풀스택, REST API, Vue.js SPA까지  
매 프로젝트마다 기술 스택을 확장해가며 성장한 과정을 담고 있습니다.

> 각 프로젝트는 2인 페어로 진행했습니다. 폴더별 회고 README는 제가 작성했고, 다른 이름(`sb`·`jw`·`jin`)이 붙은 README는 페어의 회고입니다.

---

## 📂 프로젝트 목록

| # | 프로젝트 | 핵심 기술 | 설명 |
|:---:|:---|:---|:---|
| 01 | Python 입문 | `Python` `LLM 프롬프팅` | 예금·날씨 데이터 분석 실습, AI 프롬프트 엔지니어링 적용 |
| 02 | 주가 데이터 분석 | `Python` `Pandas` `Matplotlib` | Netflix 주가 데이터 전처리·시계열 시각화·추세 분석 |
| 03 | 프로필 페이지 | `HTML` `Bootstrap` | Bootstrap 그리드 시스템을 활용한 반응형 프로필 페이지 구현 |
| 04 | 영화 정보 관리 서비스 | `Django` `SQLite` | Django CRUD 기반 영화 정보 등록·수정·삭제 서비스 |
| 05 | 금융 자산 토론 게시판 | `Django` `LLM` | 커스텀 유저 모델, 관심 종목 선택, 게시글 기반 LLM 투자 성향 분석 |
| 06 | 투자자 댓글 수집·정제 서비스 | `Django` `Selenium` `Pandas` | 토스증권 댓글 크롤링 → 패턴 필터·IQR 정제 → 규칙 기반 증강, 단계별 저장 |
| 07 | Fin Navigator | `Django` `DRF` `Kakao API` `공공데이터 API` | 금융 상품 추천 서비스, 하버사인 공식 기반 거리 가산점 (회고만 수록, 코드 미포함) |
| 08 | 금융 상품 조회 API | `Django REST Framework` `금융감독원 API` | DRF Serializer 기반 예금 상품 데이터 저장·조회 REST API |
| 09 | AI 프록시 서버 | `Django` `DRF` `FastAPI` `GMS API` | FastAPI 모델 서버 앞단 Django 프록시, 대화·이미지 생성 엔드포인트 분리, 실패 시 기본 응답 |
| 10 | 은행 위치 지도 서비스 | `JavaScript` `Kakao Map API` | 카카오맵 API 연동, 마커 표시 및 경로 시각화 |
| 12 | 관심 종목 영상 검색 서비스 | `Vue 3` `YouTube API` | Vue Router 기반 SPA, 키워드 명령 입력으로 유튜브 영상 검색·저장 |

---

## 🛠 기술 스택

| 분류 | 기술 |
|:---:|:---|
| Language | Python, JavaScript |
| Backend | Django, Django REST Framework |
| Frontend | Vue.js 3, HTML, Bootstrap, CSS |
| Data | Pandas, Matplotlib, Selenium |
| AI / LLM | OpenAI API, GMS API |
| External API | 금융감독원 Open API, Kakao Local API, Kakao Map API, YouTube Data API |
| DB | SQLite |

---

## 📈 성장 흐름

```
Python 기초 · 프롬프팅
       ↓
데이터 분석 (Pandas · Matplotlib)
       ↓
HTML · CSS · Bootstrap
       ↓
Django CRUD → Django 인증 · 커스텀 모델 · LLM 연동
       ↓
크롤링 + 데이터 정제 (Selenium · Pandas)
       ↓
풀스택 금융 서비스 (DRF · 공공 API · Kakao API)
       ↓
AI 프록시 서버 (Django → FastAPI)
       ↓
Vue 3 SPA
```
