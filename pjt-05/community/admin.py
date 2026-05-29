from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("nickname", "interest_stocks", "profile_image")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("추가 정보", {"fields": ("nickname", "interest_stocks", "profile_image")}),
    )
    list_display = ("username", "nickname", "email", "is_staff")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "asset_id", "author", "created_at")
    list_filter = ("asset_id",)
    search_fields = ("title", "content", "author")
