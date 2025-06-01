from django.apps import AppConfig


class MyAccountConfig(AppConfig):
    model_id_field = 'django.db.models.BigAutoField'
    name = 'users'

    # @property
    # def default_auto_field(self):
    #     return self.model_id_field

    # @property
    # def name(self):
    #     return self.app_label
