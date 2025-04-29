from django.apps import AppConfig


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainPage'

def ready(self):
    import mainPage.signals  # make sure signals.py exists if placed there
