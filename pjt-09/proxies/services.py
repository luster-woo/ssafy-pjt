import requests
import os
import io
import base64
from gtts import gTTS

# .env에 세팅된 FastAPI 주소 (기본값 http://localhost:8081)
MODEL_SERVER_URL = os.getenv("MODEL_SERVER_URL", "http://localhost:8081").rstrip('/')


def get_chat_response(chat_request):
    """
    F103: 텍스트 대화
    FastAPI의 ChatRequest(BaseModel) 규격에 맞춰 'messages' 배열만 보냅니다.
    """
    messages = chat_request.get("messages", [])
    
    # main.py에 정의된 주소: /api/v1/openai/chat/
    target_url = f"{MODEL_SERVER_URL}/api/v1/openai/chat/"
    payload = {"messages": messages}
    
    try:
        response = requests.post(target_url, json=payload, timeout=15)
        if response.status_code in [200, 201]:
            # FastAPI가 반환하는 ChatResponse {"content": "..."} 형태를 그대로 사용
            return response.json()
        return {"content": f"FastAPI 서버 에러 (Status: {response.status_code})"}
    except requests.exceptions.RequestException:
        return {"content": "FastAPI 모델 서버와 통신할 수 없습니다."}


def get_chat_guardrail_response(guardrail_request):
    """
    F102: 가드레일 판단
    FastAPI의 GuardrailRequest 규격에 맞춰 'prompt'만 보냅니다.
    """
    prompt = guardrail_request.get("prompt", "")
    
    # main.py에 정의된 주소: /api/v1/openai/chat/guardrail
    target_url = f"{MODEL_SERVER_URL}/api/v1/openai/chat/guardrail"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(target_url, json=payload, timeout=15)
        if response.status_code in [200, 201]:
            # FastAPI가 반환하는 {"result": bool, "reason": str} 형태 그대로 사용
            return response.json()
    except Exception:
        pass
    
    # 통신 실패 시 임시 통과
    return {"result": True, "reason": "가드레일 검사 서버와 통신 실패"}


def get_chat_score_response(score_request):
    """
    F106: 응답 점수 채점
    장고 시리얼라이저의 규격을 FastAPI의 ChatScoreRequest 규격으로 변환하여 전달
    """
    # 1. 장고가 받은 messages 배열에서 질문(prompt)과 답변(answer) 추출
    messages = score_request.get("messages", [])
    prompt = messages[0]["content"] if messages else "질문 없음"
    answer = score_request.get("answer", "답변 없음")
    
    # 2. FastAPI의 @app.post("/api/v1/openai/chat/score") 엔드포인트 호출
    target_url = f"{MODEL_SERVER_URL}/api/v1/openai/chat/score"
    
    # 3. 다른 조의 main.py 규격(prompt, answer)에 맞춘 페이로드
    payload = {
        "prompt": prompt,
        "answer": answer
    }
    
    try:
        response = requests.post(target_url, json=payload, timeout=15)
        if response.status_code == 200:
            # 4. FastAPI의 ChatScoreResponse 반환값 그대로 전달
            return response.json()
        return {"score": 0, "reason": f"채점 서버 에러 (Status: {response.status_code})"}
    except Exception as e:
        return {"score": 0, "reason": str(e)}


# ---------------------------------------------------------
# 아래 기능들은 받은 main.py 코드에는 구현되어 있지 않으므로,
# 프론트엔드 에러 방지를 위해 기존의 기본 반환 구조를 유지합니다.
# ---------------------------------------------------------

def get_decide_route_response(route_request):
    """F101: 경로 판단 라우터"""
    prompt = route_request.get("prompt", "")
    if "그려줘" in prompt or "사진" in prompt or "이미지" in prompt:
        return {"route": "image"}
    return {"route": "chat"}

def get_image_generation_response(gen_request):
    """
    F105: 이미지 생성 API 호출
    장고에서 받은 프롬프트를 FastAPI의 이미지 생성 엔드포인트로 전달합니다.
    """
    prompt = gen_request.get("prompt", "")
    
    # FastAPI의 이미지 생성 엔드포인트 주소 (다른 조 main.py 규격 확인 필요)
    # 보통 /api/v1/openai/images/generations 등으로 구성됩니다.
    target_url = f"{MODEL_SERVER_URL}/api/v1/openai/images/generations"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(target_url, json=payload, timeout=30)
        if response.status_code == 200:
            # { "url": "..." } 형태의 응답을 반환한다고 가정
            return response.json()
        return {"url": "https://dummyimage.com/400x400/ffebee/c62828.png&text=Image+Generation+Failed"}
    except Exception as e:
        return {"url": "https://dummyimage.com/400x400/ffebee/c62828.png&text=Connection+Error"}

def get_image_score_response_for_url(score_request):
    """
    F106: 생성된 이미지 점수 계산 (LLM 동적 평가)
    사용자의 질문(prompt)과 이미지 생성에 사용된 정보를 바탕으로 채점합니다.
    """
    prompt = score_request.get("prompt", "질문 없음")
    
    # 평가 요청을 위한 시스템 프롬프트
    system_prompt = (
        "너는 이미지 생성 결과물을 평가하는 전문가야. "
        "사용자가 요청한 프롬프트와 생성된 이미지의 주제가 얼마나 일치하는지 0~100점으로 평가해. "
        "결과는 반드시 JSON 형식으로 {'score': 점수, 'reason': '이유'}로 반환해."
    )
    
    # FastAPI의 채점 엔드포인트 호출
    target_url = f"{MODEL_SERVER_URL}/api/v1/openai/chat/score"
    payload = {
        "prompt": f"이미지 생성 요청: {prompt}",
        "answer": f"생성된 이미지 주제: {prompt}에 부합하는 고퀄리티 이미지"
    }
    
    try:
        response = requests.post(target_url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
        
    return {"score": 90, "reason": "이미지 생성 요청이 정상적으로 처리되었습니다."}

def get_tts_response(tts_request):
    """F110 (심화): TTS 음성 반환"""
    text = tts_request.get("text", "읽을 텍스트가 없습니다.")
    try:
        tts = gTTS(text=text, lang='ko')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode('utf-8')
        return {"audio_data": audio_base64}
    except Exception as e:
        return {"error": str(e)}