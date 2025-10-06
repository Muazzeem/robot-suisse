import uuid

from django.db import models

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
)

from home.choices import ROBOTS_CHOICES

class BaseModel(models.Model):
    class Meta:
        abstract = True

class UUIDBaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True

class TimeStampModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ActiveTimeStampModel(TimeStampModel):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class ActiveObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class BasePage(Page):
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    og_keywords = models.CharField(
        _("Og keywords"), max_length=550, null=True, blank=True
    )
    robots_directive = models.CharField(
        max_length=20,
        choices=ROBOTS_CHOICES,
        default="index, follow",
        help_text="Meta robots tag for SEO",
    )

    # Add this line
    api_fields = []

    promote_panels = Page.promote_panels + [
        FieldPanel("og_image", help_text="size: width-1200px, height-630px"),
        FieldPanel("og_keywords"),
        FieldPanel("robots_directive"),
    ]

    class Meta:
        abstract = True