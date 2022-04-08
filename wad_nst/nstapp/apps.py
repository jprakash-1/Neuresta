from django.apps import AppConfig


class NstappConfig(AppConfig):
    name = 'nstapp'

    def ready(self):
        import nstapp.signals