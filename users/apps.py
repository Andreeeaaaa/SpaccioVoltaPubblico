from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Ready function to import the signals file in
    def ready(self) -> None:
        import users.signals
