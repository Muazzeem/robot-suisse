from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel
)
from wagtail.api import APIField
from wagtail.fields import StreamField
from .choices import ROBOTS_CHOICES
from .blocks import *
from .fields import ImageRenditionField


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

    api_fields = []

    promote_panels = Page.promote_panels + [
        FieldPanel("og_image", help_text="size: width-1200px, height-630px"),
        FieldPanel("og_keywords"),
        FieldPanel("robots_directive"),
    ]

    class Meta:
        abstract = True

class HomePage(BasePage):
    parent_page_types = []
    subpage_types = ["home.BlogIndexPage", "home.RobotIndexPage"]

    content_panels = Page.content_panels + []

    def get_context(self, request):
        context = super().get_context(request)
        context["og_image"] = self.og_image
        return context



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

    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "home.BlogCategoryPage",
    ]


class BlogCategoryPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("title_ar")]

    parent_page_types = [
        "home.BlogIndexPage",
    ]
    subpage_types = [
        "home.BlogDetailPage",
    ]


from rest_framework import serializers
from .fields import ImageSerializerField


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

    body = StreamField([
                ("title", TitleBlock()),
                ("banner_image", BannerImageBlock()),
                ("banner_video", BannerVideoBlock()),
                ("two_images", TwoImageBlock()),
                ("carousel", ImageCarouselBlock()),
                ("richtext", RichtextBlock()),
                ("faq", FaqBlock()),
                ("media_text", MediaTextBlock()),
                # ("specifications", SpecificationBlock()),
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
                FieldPanel("body"),
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


class RobotCategoryPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("title_ar")]

    parent_page_types = [
        "home.RobotIndexPage",
    ]
    subpage_types = [
        "home.RobotDetailsPage",
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
        "home.RobotCategoryPage",
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
    tags = models.JSONField(blank=True, null=True)

    body = StreamField([
                ("title", TitleBlock()),
                ("banner_image", BannerImageBlock()),
                ("banner_video", BannerVideoBlock()),
                ("two_images", TwoImageBlock()),
                ("carousel", ImageCarouselBlock()),
                ("richtext", RichtextBlock()),
                ("faq", FaqBlock()),
                ("media_text", MediaTextBlock()),
            ],
        null=True,
        blank=True,
        use_json_field=True,
    )


    content_panels = Page.content_panels + [
        FieldPanel("is_featured"),
        FieldPanel("name_en"),
        FieldPanel("name_de_ch"),
        FieldPanel("name_fr_ch"),
        FieldPanel("name_it_ch"),
        FieldPanel("status"),
        FieldPanel("brand"),
        FieldPanel("tags"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.RobotCategoryPage"]
    subpage_types = []

    api_fields = BasePage.api_fields + [
        APIField("name_en"),
        APIField("name_de_ch"),
        APIField("name_fr_ch"),
        APIField("name_it_ch"),
        APIField("status"),
        APIField("brand"),
        APIField("tags"),
        APIField("body"),
    ]
