from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "actnow.profiles"

    def ready(self):
        import actnow.profiles.signals  # NOQA
