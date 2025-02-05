from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-updating
    created_at and updated_at fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
