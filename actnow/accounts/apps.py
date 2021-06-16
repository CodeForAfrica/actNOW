from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "actnow.accounts"

    def ready(self):
        import actnow.accounts.signals  # NOQA
