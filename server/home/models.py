from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BasePage
from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.api import APIField

from .fields import ImageRenditionField, ImageSerializerField
from .forms import *
from . import blocks


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=250)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("image"),
            ],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.name


class HomePage(BasePage):
    template = "home/home.html"

    parent_page_types = []
    subpage_types = [
        "ContactPage", "BlogIndexPage", "PublicPage", 
        "company.CompanyIndexPage", "robot.RobotIndexPage"
    ]


class ContactPage(BasePage):
    template = "home/contact.html"

    parent_page_types = ["HomePage"]
    subpage_types = []


class PublicPage(BasePage):
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Cover Image"),
        help_text=_("Cover image for the service detail page"),
    )

    body = StreamField(
        blocks.COMMON_BLOCKS,
        use_json_field=True,
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        MultiFieldPanel([FieldPanel("body")], heading="Body Content"),
    ]

    parent_page_types = ["home.HomePage"]  # ensure correct app label
    subpage_types = []

    class Meta:
        verbose_name = "Public Page"
        verbose_name_plural = "Public Pages"



class BlogIndexPage(BasePage):
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
        from .serializers import BlogCategoryPageSerializer

        childs = self.get_children()
        return BlogCategoryPageSerializer(childs, many=True).data

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

    parent_page_types = ["HomePage"]
    subpage_types = [
        "BlogCategoryPage",
    ]


class BlogCategoryPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("title_ar")]

    parent_page_types = [
        "BlogIndexPage",
    ]
    subpage_types = [
        "BlogDetailPage",
    ]


from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    image = ImageSerializerField()

    class Meta:
        model = Author
        fields = "__all__"


class BlogDetailPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    body = StreamField(
        [
            ("title", blocks.TitleBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(
        "Author",
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(_("Featured blog"), default=False)
    tags = models.CharField(
        _("Tags: Comma separated"), max_length=250, null=True, blank=True
    )
    short_description = models.TextField(_("Short description"), null=True, blank=True)
    short_description_ar = models.TextField(
        _("Short description ar"), null=True, blank=True
    )

    @property
    def fetch_parent(self):
        obj = self.get_parent()
        return {
            "id": obj.specific.id,
            "title": obj.specific.title,
            "title_ar": obj.specific.title_ar,
            "slug": obj.specific.slug,
        }
    
    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
        MultiFieldPanel(
            [
                FieldPanel("short_description"),
                FieldPanel("short_description_ar"),
                FieldPanel("is_featured"),
                FieldPanel("tags"),
                FieldPanel("thumbnail", help_text="252x372 pixel"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("author"),
            ],
            heading="Author",
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]
    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_ar"),
        APIField("short_description"),
        APIField("short_description_ar"),
        APIField(
            "thumbnail",
            serializer=ImageRenditionField(
                {"original": "original|jpegquality-80|format-webp"}
            ),
        ),
        APIField("author", serializer=AuthorSerializer()),
        APIField("last_published_at"),
        APIField("body"),
        APIField("tags"),
        APIField("is_featured"),
        APIField("fetch_parent"),
    ]

    parent_page_types = [
        "home.BlogCategoryPage",
    ]
    subpage_types = []
    

