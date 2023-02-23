"""
This module defines the configuration for the 'DemoAppConfig' Django app.

Available configurations:
- DemoAppConfig: defines the app name and default configuration settings
"""

from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    """
    Configuration class for the 'demoapp' app.

    Attributes:
        name (str): The name of the app, as registered in the project settings.
        default_auto_field (str): The default primary key field for new models.
            This is set to 'django.db.models.AutoField' by default, but can be
            changed to another field type if desired.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "demo_app"
