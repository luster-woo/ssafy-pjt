from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException,Request

load_dotenv(".env")

GMS_KEY = os.getenv("GMS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
OPENAI_URL = "https://api.openai.com/v1"
MODE = os.getenv("MODE", "GMS")

headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Accept": "application/json",
}

gms_headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

openai_headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    content: str


app = FastAPI()

@app.post("/api/v1/openai/chat/", response_model=ChatResponse)
async def get_chat_response(chat_request: ChatRequest):
    messages = chat_request.messages

    payload_data = {"model": "gpt-5-nano", "messages": messages}
    response = requests.post(
        f"{GMS_URL}/chat/completions", headers=headers, json=payload_data
    )
    
    content = response.json()["choices"][0]["message"]["content"]
    return {"content": content}





import json

class ChatScoreRequest(BaseModel):
    prompt: str
    answer: str


class ChatScoreResponse(BaseModel):
    score: int
    reason: str




@app.post("/api/v1/openai/chat/score", response_model=ChatScoreResponse)
def get_chat_score(chat_score_request: ChatScoreRequest):
    prompt = chat_score_request.prompt
    answer = chat_score_request.answer

    messages = [
        {
            "role": "developer",
            "content": """너는 질문 prompt에 대한 답변 answer이 몇 점짜리인지 판단하는 시스템이다.
            질문에 대한 적절한 답변인지의 점수를 0 ~ 100점으로 리턴하라.
            또한, 해당 이유에 대해서도 reason에 기입한다."""
        },
        {
            "role": "user", "content": f"prompt: {prompt}, answer: {answer}"
        }
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "score_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "integer",
                        "description": "질문에 대한 답변 점수를 0점부터 100점 사이로 반환",
                    },
                    "reason": {
                        "type": "string",
                        "description": "score 가 도출된 이유에 대해 간단한 설명",
                    },
                },
                "required": ["score", "reason"],
                "additionalProperties": False,
            },
        },
    }

    payload_data = {"model": "gpt-5-nano", "messages": messages, "response_format": response_format,}
    response = requests.post(f"{GMS_URL}/chat/completions", headers=headers, json=payload_data)
    res_data = response.json()

    content_str = res_data["choices"][0]["message"]["content"]
    
    result = json.loads(content_str)
    return result




class GuardrailRequest(BaseModel):
    prompt: str


class GuardrailResponse(BaseModel):
    result: bool
    reason: str

@app.post("/api/v1/openai/chat/guardrail", response_model=GuardrailResponse)
def get_guardrail_response(guardrail_request: GuardrailRequest):
    prompt = guardrail_request.prompt

    system_content = """
        너는 질문 prompt 가 적절한지 판단하는 Guardrail 이다.
        질문이 적절한지 여부를 result 에 boolean 으로 응답하라.
        기준은 선정성과 법률 위배 가능성이다.
        그리고 그렇게 판단한 이유를 reason 에 기입하라.
    """
    messages = [
        {"role": "developer", "content": system_content},
        {"role": "user", "content": f"prompt: {prompt}"},
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "guardrail_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "boolean",
                        "description": "사용자의 prompt 가 적절한지 여부",
                    },
                    "reason": {
                        "type": "string",
                        "description": "result 가 도출된 이유",
                    },
                },
                "required": ["result", "reason"],
                "additionalProperties": False,
            },
        },
    }

    payload_data = {"model": "gpt-5-nano", "messages": messages, "response_format": response_format}


    response = requests.post(f"{GMS_URL}/chat/completions",headers=headers, json=payload_data)

    result_dict = json.loads(response.json()["choices"][0]["message"]["content"])
    result = result_dict["result"]
    reason = result_dict["reason"]
    return {"result": result, "reason": reason}


# 이미지 생성 요청을 위한 전용 모델 설정 및 엔드포인트
@app.post("/api/v1/openai/images/generations")
async def get_image_generation(request: Request):
    """
    F105: 텍스트 모델이 아닌 이미지 생성 모델(DALL-E 등)로 분기 처리
    """
    payload = await request.json()
    
    # 이미지 생성은 모델을 'dall-e-3' 등으로 명시해야 합니다.
    payload_data = {
        "prompt": payload.get("prompt"),
        "n": 1,
        "size": "1024x1024"
    }
    
    # GMS 서버의 이미지 엔드포인트 호출 (텍스트와 경로가 다름을 주의!)
    response = requests.post(
        f"{GMS_URL.replace('/chat/completions', '')}/images/generations", 
        headers=headers, 
        json=payload_data
    )
    
    return response.json()