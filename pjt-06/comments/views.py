from django.shortcuts import render

from .models import CommentRun
from .services import augment_comments, clean_comments, fetch_toss_comments


def index(request):
    context = {
        'latest_runs': CommentRun.objects.all()[:5],
    }

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        context['company_name'] = company_name

        if not company_name:
            context['error'] = '회사명을 입력해 주세요.'
            return render(request, 'comments/index.html', context)

        try:
            crawl_result = fetch_toss_comments(company_name)
            clean_result = clean_comments(crawl_result.comments)
            augmented_comments = augment_comments(clean_result.comments)
            run = CommentRun.objects.create(
                query_name=company_name,
                matched_company_name=crawl_result.matched_company_name,
                stock_code=crawl_result.stock_code,
                original_comments=crawl_result.comments,
                cleaned_comments=clean_result.comments,
                augmented_comments=augmented_comments,
                iqr_lower=clean_result.lower,
                iqr_upper=clean_result.upper,
            )
            context['run'] = run
            context['latest_runs'] = CommentRun.objects.all()[:5]
        except RuntimeError as exc:
            context['error'] = str(exc)

    return render(request, 'comments/index.html', context)
