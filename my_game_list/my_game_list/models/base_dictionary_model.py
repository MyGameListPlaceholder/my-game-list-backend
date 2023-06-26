"""This module contains the base dictionary model for all dictionary models in the application."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseDictionaryModel(models.Model):
    """Base class for all dictionary models."""

    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        """Meta data for dictionary models."""

        abstract = True
        ordering = ("id",)

    def __str__(self: "BaseDictionaryModel") -> str:
        """String representation of dictionary models."""
        return self.name
