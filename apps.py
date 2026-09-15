from django.apps import AppConfig

class PlatformLogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'platform_logic'

    def ready(self):
        import platform_logic.signals
