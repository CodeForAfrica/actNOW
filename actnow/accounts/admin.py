from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from .forms import ActNowUserChangeForm, ActNowUserCreationForm
from .models import ActNowUser


class ActNowUserAdmin(UserAdmin):
    add_form = ActNowUserCreationForm
    form = ActNowUserChangeForm
    model = ActNowUser
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "groups")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class ActNowAdminSite(AdminSite):
    site_header = "ActNow administration"
    site_title = "ActNow"
    login_template = "login.html"


admin_site = ActNowAdminSite("admin")

admin_site.register(ActNowUser, ActNowUserAdmin)
admin_site.register(Group, GroupAdmin)
