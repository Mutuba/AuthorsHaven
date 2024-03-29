from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = "authors.apps.authentication"
    label = "authentication"

    def ready(self):
        import authors.apps.authentication.signals


default_app_config = "authors.apps.authentication.AuthenticationAppConfig"
