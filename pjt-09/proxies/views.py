"""
교육생 구현 영역: 각 뷰에서 serializer로 검증 후 services 함수를 호출하고,
결과를 적절한 HTTP 상태 코드와 함께 반환하세요.
chat_response 는 예시로 구현되어 있습니다. 나머지는 pass 를 채워 구현하세요.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# 1. 사용할 Serializer 모두 가져오기
from proxies.serializers import (
    ChatRequestSerializer, ChatResponseSerializer,
    ChatGuardrailRequestSerializer, ChatGuardrailResponseSerializer,
    ChatScoreRequestSerializer, ChatScoreResponseSerializer,
    ImageGenerationRequestSerializer, ImageGenerationResponseSerializer,
    ImageScoreRequestForImageURLSerializer, ImageScoreResponseForImageURLSerializer,
    DecideRouteRequestSerializer, DecideRouteResponseSerializer,
    GenerateSpeechRequestSerializer, GenerateSpeechResponseSerializer
)

# 2. 사용할 Service 함수 모두 가져오기
from proxies.services import (
    get_chat_response,
    get_chat_guardrail_response,
    get_chat_score_response,
    get_image_generation_response,
    get_image_score_response_for_url,
    get_decide_route_response,
    get_tts_response
)
from django.shortcuts import render

def chatbot_home(request):
    return render(request, 'proxies/index.html')

@api_view(["POST"])
def chat_response(request):
    """예시: 채팅 완성 요청을 중간 서버가 모델 서버로 전달합니다."""
    serializer = ChatRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_chat_response(serializer.validated_data)

        if result is None:
            return Response(
                {"detail": "Chat response failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(ChatResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def chat_guardrail_response(request):
    """F102: 가드레일 검증 수행 후 적절성 여부에 따라 201 또는 403 반환"""
    serializer = ChatGuardrailRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_chat_guardrail_response(serializer.validated_data)

        if result is None:
            return Response({"detail": "Guardrail check failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 방금 수정한 시리얼라이저의 'result' 키값을 기준으로 분기합니다.
        if result.get("result") is True:
            return Response(ChatGuardrailResponseSerializer(result).data, status=status.HTTP_201_CREATED)
        else:
            return Response(ChatGuardrailResponseSerializer(result).data, status=status.HTTP_403_FORBIDDEN)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def chat_score_response(request):
    """F106: 텍스트 답변에 대한 점수 계산 요청 전달"""
    serializer = ChatScoreRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_chat_score_response(serializer.validated_data)

        if result is None:
            return Response({"detail": "Chat score calculation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(ChatScoreResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def image_generation_response(request):
    """F105: 이미지 생성 요청 전달"""
    serializer = ImageGenerationRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_image_generation_response(serializer.validated_data)

        if result is None:
            return Response({"detail": "Image generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(ImageGenerationResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def image_score_response_for_url(request):
    """F106: 생성된 이미지 URL에 대한 점수 계산 요청 전달"""
    serializer = ImageScoreRequestForImageURLSerializer(data=request.data)

    if serializer.is_valid():
        result = get_image_score_response_for_url(serializer.validated_data)

        if result is None:
            return Response({"detail": "Image score calculation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(ImageScoreResponseForImageURLSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def decide_route_response(request):
    """F101: 사용자의 prompt를 분석해 chat/image 경로 판단 요청 전달"""
    serializer = DecideRouteRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_decide_route_response(serializer.validated_data)

        if result is None:
            return Response({"detail": "Route decision failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(DecideRouteResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def tts_response(request):
    """F110 (심화): TTS 음성 생성 요청 전달"""
    serializer = GenerateSpeechRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_tts_response(serializer.validated_data)

        if result is None:
            return Response({"detail": "TTS generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(GenerateSpeechResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)