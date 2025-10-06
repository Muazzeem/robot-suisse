from django.db import models
from rest_framework import serializers

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from django.utils.translation import gettext_lazy as _

from core.models import BasePage
from company.models import CompanyDetailsPage


class RobotCategoryPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("title_ar")]

    parent_page_types = [
        "RobotIndexPage",
    ]
    subpage_types = [
        "RobotDetailsPage",
    ]


class RobotCategoryPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotCategoryPage
        fields = ("id", "title", "title_ar", "slug")


class RobotIndexPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)
    hero_title = models.CharField(
        _("Hero title"), max_length=250, null=True, blank=True
    )
    hero_title_ar = models.CharField(
        _("Hero title ar"), max_length=250, null=True, blank=True
    )
    hero_subtitle = models.CharField(
        _("Hero subtitle"), max_length=250, null=True, blank=True
    )
    hero_subtitle_ar = models.CharField(
        _("Hero subtitle ar"), max_length=250, null=True, blank=True
    )

    @property
    def categories(self):

        childs = self.get_children()
        return RobotCategoryPageSerializer(childs, many=True).data

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
        FieldPanel("hero_title"),
        FieldPanel("hero_title_ar"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_subtitle_ar"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_ar"),
        APIField("categories"),
        APIField("hero_title"),
        APIField("hero_title_ar"),
        APIField("hero_subtitle"),
        APIField("hero_subtitle_ar"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "RobotCategoryPage",
    ]


class RobotDetailsPage(BasePage):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("upcoming", "Upcoming"),
        ("archived", "Archived"),
    ]

    is_featured = models.BooleanField(default=False, help_text="Featured robots will be displayed on the homepage.")
    name_en = models.CharField(max_length=255)
    name_de_ch = models.CharField(max_length=255, blank=True, null=True)
    name_fr_ch = models.CharField(max_length=255, blank=True, null=True)
    name_it_ch = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    brand = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(
        CompanyDetailsPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="robots",
    )
    tags = models.JSONField(blank=True, null=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("name_en"),
        FieldPanel("name_de_ch"),
        FieldPanel("name_fr_ch"),
        FieldPanel("name_it_ch"),
        FieldPanel("status"),
        FieldPanel("brand"),
        FieldPanel("company"),
        FieldPanel("tags"),
    ]

    parent_page_types = ["robot.RobotCategoryPage"]
    subpage_types = []

    api_fields = BasePage.api_fields + [
        APIField("name_en"),
        APIField("name_de_ch"),
        APIField("name_fr_ch"),
        APIField("name_it_ch"),
        APIField("status"),
        APIField("brand"),
        APIField("company"),
        APIField("tags"),
    ]
