from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from .utils import load_assets


def get_interest_stock_choices():
    return [(asset["id"], asset["name"]) for asset in load_assets()]


class SignUpForm(UserCreationForm):
    nickname = forms.CharField(label="닉네임", max_length=150)
    profile_image = forms.ImageField(label="프로필 이미지", required=False)
    interest_stocks = forms.MultipleChoiceField(
        label="관심 종목",
        required=False,
        choices=(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "nickname", "profile_image", "interest_stocks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "아이디"
        self.fields["password1"].label = "비밀번호"
        self.fields["password2"].label = "비밀번호 확인"
        self.fields["interest_stocks"].choices = get_interest_stock_choices()
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not username:
            raise forms.ValidationError("아이디를 입력해 주세요.")
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용 중인 아이디입니다.")
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"].strip()
        if not nickname:
            raise forms.ValidationError("닉네임을 입력해 주세요.")
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data["nickname"]
        user.interest_stocks = ",".join(self.cleaned_data.get("interest_stocks", []))
        profile_image = self.cleaned_data.get("profile_image")
        if profile_image:
            user.profile_image = profile_image
        if commit:
            user.save()
        return user


class KoreanAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="아이디")
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "아이디 또는 비밀번호가 올바르지 않습니다.",
        "inactive": "비활성화된 계정입니다.",
    }


class KoreanPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_incorrect": "현재 비밀번호가 올바르지 않습니다.",
        "password_mismatch": "새 비밀번호와 비밀번호 확인이 일치하지 않습니다.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "현재 비밀번호"
        self.fields["new_password1"].label = "새 비밀번호"
        self.fields["new_password2"].label = "새 비밀번호 확인"
        self.fields["new_password1"].help_text = ""
        self.fields["new_password2"].help_text = ""
