from django.apps import AppConfig

class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_auth'   # THIS STAYS as Python import path
    label = 'user_auth'       # THIS is the app_label Django uses
