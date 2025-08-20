from django.apps import AppConfig


class SecretariaescolarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'secretariaescolar'

    def ready(self):
        import secretariaescolar.signals
