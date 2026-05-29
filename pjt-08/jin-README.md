금융 상품 데이터를 활용한 REST API Server 구축
1. 프로젝트 개요
프로젝트명: 금융 상품 비교 애플리케이션 (8회차 관통 프로젝트)
개발 환경: Python, Django, Django REST Framework, SQLite3, Requests, OpenAI API, django-environ
팀 구성 및 역할: 2인 1조 팀 프로젝트
본인 (팀원 A): 데이터 파이프라인 구축(외부 API 연동 및 DB 적재), AI 기반 더미 데이터 생성
팀원 B: 조회 및 조작 엔드포인트 구현 (특정 옵션 조회, 최고 금리 상품 조회 등)
협업 방식: Git Feature Branch 전략을 활용한 병렬 개발 및 Merge Request 기반 코드 리뷰
2. 새로 배운 내용 (학습 내용)
API Key 보안 관리: .env 파일과 django-environ 패키지를 활용하여 금융감독원 및 OpenAI의 API Key를 하드코딩하지 않고 분리하여 관리하는 방법을 익혔으며, .gitignore를 통해 외부에 노출되지 않도록 하는 보안의 기본을 다졌습니다.
RESTful API 아키텍처: 단순히 HTML을 반환하는 서버가 아닌, 클라이언트와 JSON 포맷으로 데이터를 주고받는 진정한 의미의 백엔드 API 서버 구조를 이해했습니다.
Git Branch 협업 전략: 마이그레이션 충돌이라는 '지옥'을 피하기 위해 뼈대(Skeleton) 코드를 먼저 완성하여 Main에 올린 뒤, 기능별로 feature/ 브랜치를 분기하여 작업하고 합치는 실무적인 협업 워크플로우를 체득했습니다.
3. 어려웠던 점 및 해결 방법
"미등록 인증키" 및 빈 데이터 이슈:
문제: F801 구현 중 서버 응답이 빈 리스트([])로 오거나 400 에러가 발생하는 현상이 있었습니다.
해결: print(response.json())을 통해 실제 반환되는 에러 메시지를 추적했습니다. .env 파일 작성 시 파이썬 문법처럼 따옴표("")를 넣어서 발생한 파싱 오류임을 깨닫고, 따옴표를 제거한 뒤 서버를 재시작하여 정상적으로 데이터를 수신할 수 있었습니다.
Serializer 유효성 검사 반려:
문제: F803 POST 테스트 중 필수 필드(etc_note) 누락으로 인해 400 Bad Request가 발생했습니다.
해결: 모델 설계 시 모든 필드가 필수로 지정되었기 때문임을 파악하고, serializers.py의 extra_kwargs에 {'required': False, 'allow_blank': True} 옵션을 추가하여 데이터 입력의 유연성을 확보했습니다.
ModuleNotFoundError 오타 디버깅:
초기 세팅 중 settings.py의 INSTALLED_APPS에 finlife를 finfile로 오타 내어 서버가 실행되지 않는 문제를 겪었으며, 꼼꼼한 코드 리뷰와 에러 트레이스백 읽기의 중요성을 다시금 느꼈습니다.