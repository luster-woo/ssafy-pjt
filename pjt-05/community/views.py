from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import KoreanAuthenticationForm, KoreanPasswordChangeForm, SignUpForm
from .llm import build_investment_analysis
from .models import Post
from .utils import get_asset_by_id, load_assets


class UserLoginView(LoginView):
    template_name = "community/login.html"
    authentication_form = KoreanAuthenticationForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "community/password_change.html"
    form_class = KoreanPasswordChangeForm
    success_url = reverse_lazy("community:password_change_done")


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "community/password_change_done.html"


def asset_list(request):
    assets = load_assets()
    return render(request, "community/asset_list.html", {"assets": assets})


def board(request, asset_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    posts = Post.objects.filter(asset_id=asset_id)
    return render(request, "community/board.html", {"asset": asset, "posts": posts})


def post_detail(request, asset_id, post_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    is_author = request.user.is_authenticated and request.user.username == post.author
    context = {"asset": asset, "post": post, "is_author": is_author}
    return render(request, "community/post_detail.html", context)


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("community:asset_list")

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("community:asset_list")
    else:
        form = SignUpForm()

    return render(request, "community/signup.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    assets = {asset["id"]: asset["name"] for asset in load_assets()}
    interest_stock_ids = [item for item in user.interest_stocks.split(",") if item]
    interest_stock_names = [assets.get(stock_id, stock_id) for stock_id in interest_stock_ids]
    posts = [
        {
            "id": post.id,
            "title": post.title,
            "asset_id": post.asset_id,
            "asset_name": assets.get(post.asset_id, post.asset_id),
            "created_at": post.created_at,
        }
        for post in Post.objects.filter(author=user.username)
    ]
    context = {
        "profile_user": user,
        "interest_stock_names": interest_stock_names,
        "posts": posts,
    }
    return render(request, "community/profile.html", context)


@login_required
def profile_analysis(request):
    user_posts = list(Post.objects.filter(author=request.user.username).order_by("-created_at"))
    analysis_result = build_investment_analysis(user_posts)

    context = {
        "post_count": len(user_posts),
        "analysis_result": analysis_result,
    }
    return render(request, "community/profile_analysis.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request, asset_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if title and content:
            Post.objects.create(
                asset_id=asset_id,
                title=title,
                content=content,
                author=request.user.username,
            )
            messages.success(request, "게시글이 등록되었습니다.")
            return redirect("community:board", asset_id=asset_id)

        messages.error(request, "제목과 내용을 모두 입력해 주세요.")

    return render(request, "community/post_form.html", {"asset": asset})


def ensure_post_author(request, post, asset_id):
    if request.user.username != post.author:
        messages.error(request, "작성자 본인만 수정 또는 삭제할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)
    return None


@login_required
@require_http_methods(["GET", "POST"])
def post_update(request, asset_id, post_id):
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    denied_response = ensure_post_author(request, post, asset_id)
    if denied_response:
        return denied_response

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, "게시글이 수정되었습니다.")
            return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

        messages.error(request, "제목과 내용을 모두 입력해 주세요.")

    context = {
        "asset": asset,
        "post": post,
        "title": post.title,
        "content": post.content,
        "is_edit": True,
    }
    return render(request, "community/post_form.html", context)


@login_required
@require_http_methods(["POST"])
def post_delete(request, asset_id, post_id):
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    denied_response = ensure_post_author(request, post, asset_id)
    if denied_response:
        return denied_response

    post.delete()
    messages.success(request, "게시글이 삭제되었습니다.")
    return redirect("community:board", asset_id=asset_id)
