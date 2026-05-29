from django.conf import settings
from openai import OpenAI


ANALYSIS_SYSTEM_PROMPT = """
당신은 금융 커뮤니티 사용자의 게시글 활동을 바탕으로 투자 성향을 요약하는 분석가입니다.

반드시 아래 형식으로만 한국어로 답변하세요.

1. 투자 성향 한줄 요약: 한 문장
2. 성향 근거:
- 근거 1
- 근거 2
- 근거 3
3. 관심 자산/시장:
- 항목 1
- 항목 2
4. 주의할 점:
- 항목 1
- 항목 2
5. 종합 코멘트: 두세 문장

규칙:
- 제공된 게시글 내용만 근거로 분석합니다.
- 단정적인 투자 권유는 하지 않습니다.
- 게시글이 부족하면 추측하지 말고 부족하다고 말합니다.
""".strip()


def _build_llm_client():
    mode = (getattr(settings, "MODE", "OPENAI") or "OPENAI").strip().upper()

    if mode == "UPSTAGE":
        api_key = (getattr(settings, "UPSTAGE_API_KEY", "") or "").strip()
        if not api_key:
            return None, None, "UPSTAGE_API_KEY가 설정되지 않았습니다."
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.upstage.ai/v1/solar",
        )
        model = (getattr(settings, "UPSTAGE_MODEL", "") or "").strip() or "solar-pro"
        return client, model, None

    api_key = (getattr(settings, "OPENAI_API_KEY", "") or "").strip()
    if not api_key or api_key == "<OPENAI_API_KEY>":
        return None, None, "OPENAI_API_KEY가 설정되지 않았습니다."

    client = OpenAI(api_key=api_key)
    model = (getattr(settings, "OPENAI_MODEL", "") or "").strip() or "gpt-5-nano"
    return client, model, None


def build_investment_analysis(posts):
    if len(posts) < 2:
        return {
            "ok": False,
            "message": "투자 성향 분석을 하려면 게시글이 2개 이상 필요합니다.",
        }

    joined_posts = []
    for index, post in enumerate(posts, start=1):
        title = (post.title or "").strip()
        content = (post.content or "").strip()
        if not title and not content:
            continue
        joined_posts.append(f"[게시글 {index}] 제목: {title}\n내용: {content}")

    merged_text = "\n\n".join(joined_posts).strip()
    if len(merged_text) < 80:
        return {
            "ok": False,
            "message": "게시글 내용이 너무 짧아 투자 성향을 분석하기 어렵습니다.",
        }

    client, model, error_message = _build_llm_client()
    if not client:
        return {
            "ok": False,
            "message": error_message or "LLM 클라이언트를 생성하지 못했습니다.",
        }

    user_prompt = (
        "아래 사용자의 게시글 활동을 바탕으로 투자 성향을 분석해 주세요.\n\n"
        f"{merged_text}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=700,
        )
        content = (response.choices[0].message.content or "").strip()
        if not content:
            return {
                "ok": False,
                "message": "분석 결과가 비어 있습니다. 다시 시도해 주세요.",
            }
        return {
            "ok": True,
            "content": content,
            "model": model,
        }
    except Exception as exc:
        return {
            "ok": False,
            "message": f"분석 요청 중 오류가 발생했습니다: {type(exc).__name__}",
        }
