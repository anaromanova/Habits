from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "habits_project.users"

    def ready(self):
        import habits_project.users.signals  # noqa
