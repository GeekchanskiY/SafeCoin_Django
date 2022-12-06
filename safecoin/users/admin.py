from django.contrib import admin
from .models import SCUser


@admin.register(SCUser)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'birthday', 'about_me', 'avatar', 'subscribes', 'likes')
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    readonly_fields = ('email',)
    filter_vertical = ('subscribes', 'likes')
