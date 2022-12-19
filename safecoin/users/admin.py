from django.contrib import admin
from .models import SCUser


@admin.register(SCUser)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'birthday', 'about_me', 'avatar', 'subscribes', 'likes', 'country')
    list_display = ('email', 'username',)
    search_fields = ('username', 'email', 'country')
    readonly_fields = ('email',)
    filter_vertical = ('subscribes', 'likes')
