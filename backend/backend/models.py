from django.db import models

class Enum:
    @classmethod
    def get_choices(cls):
        choices = []
        for attr_name in dir(cls):
            if not attr_name.startswith("__") and not callable(getattr(cls, attr_name)):
                choices.append((getattr(cls, attr_name), attr_name.replace("_", " ").title()))
        return choices

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True