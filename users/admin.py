from unfold.admin import ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Application, Criteria


@admin.register(User)
class UserModelAdmin(UserAdmin, ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["phone", "first_name", "last_name",]
    ordering = ["phone", ]
    model = User
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("phone", "first_name", "last_name", )
        }), 
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("phone", "password1", "password2", "first_name", "last_name", )
        }), 
    )


@admin.register(Criteria)
class CriteriaModelAdmin(ModelAdmin):
    list_display = ["name", "created", ]


@admin.register(Application)
class ApplicationModelAdmin(ModelAdmin):
    list_display = ["criteria", "author", "status", "created", ]
