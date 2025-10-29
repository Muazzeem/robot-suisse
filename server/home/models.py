from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from rest_framework import serializers

from .choices import ROBOTS_CHOICES
from .blocks import *
from .fields import ImageRenditionField, ImageSerializerField


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
            [FieldPanel("name"), FieldPanel("image")],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.name


class AuthorSerializer(serializers.ModelSerializer):
    image = ImageSerializerField()

    class Meta:
        model = Author
        fields = "__all__"

class BasePage(Page):
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    og_keywords = models.CharField(_("Og keywords"), max_length=550, null=True, blank=True)
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
    body = StreamField(
        [
            ("hero_title", HeroTitleBlock()),
            ("title", TitleBlock()),
            ("why_chose", CategoryCardsBlock()),
            ("features", FeaturesBlock()),
            ("robots", RobotsBlock()),
            ("tabs", TabsBlock()),
            ("cta", CTABlock()),
            ("categories", CategoriesBlock()),
            ("blogs", BlogsBlock()),
            ("chat", ChatBlock()),
            ("faq", FaqBlock()),
            ("contact", ContactSection()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("body")]

    parent_page_types = []
    subpage_types = [
        "home.AboutPage",
        "home.BlogIndexPage",
        "home.ContactPage",
        "home.PublicPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["og_image"] = self.og_image
        return context


# ---------------------------- Blog Pages ----------------------------

class BlogIndexPage(BasePage):
    tag_en = models.CharField(max_length=255, help_text="The tag for the page.")
    tag_dech = models.CharField(max_length=255, blank=True, null=True, help_text="German tag")
    tag_frch = models.CharField(max_length=255, blank=True, null=True, help_text="French tag")
    tag_itch = models.CharField(max_length=255, blank=True, null=True, help_text="Italian tag")

    hero_title_en = models.CharField(max_length=255)
    hero_title_dech = models.CharField(max_length=255, blank=True, null=True)
    hero_title_frch = models.CharField(max_length=255, blank=True, null=True)
    hero_title_itch = models.CharField(max_length=255, blank=True, null=True)

    hero_description_en = models.TextField(blank=True)
    hero_description_dech = models.TextField(blank=True, null=True)
    hero_description_frch = models.TextField(blank=True, null=True)
    hero_description_itch = models.TextField(blank=True, null=True)

    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    @property
    def categories(self):
        from .serializers import BlogCategoryPageSerializer

        childs = self.get_children()
        return BlogCategoryPageSerializer(childs, many=True).data

    content_panels = Page.content_panels + [
        FieldPanel("tag_en"), FieldPanel("tag_dech"), FieldPanel("tag_frch"), FieldPanel("tag_itch"),
        FieldPanel("hero_title_en"), FieldPanel("hero_title_dech"), FieldPanel("hero_title_frch"), FieldPanel("hero_title_itch"),
        FieldPanel("hero_description_en"), FieldPanel("hero_description_dech"),
        FieldPanel("hero_description_frch"), FieldPanel("hero_description_itch"),
        FieldPanel("hero_image"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("categories"),
        APIField("hero_image"),
        APIField("tag_en"), APIField("tag_dech"), APIField("tag_frch"), APIField("tag_itch"),
        APIField("hero_title_en"), APIField("hero_title_dech"), APIField("hero_title_frch"), APIField("hero_title_itch"),
        APIField("hero_description_en"), APIField("hero_description_dech"),
        APIField("hero_description_frch"), APIField("hero_description_itch"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.BlogCategoryPage"]


class BlogCategoryPage(BasePage):
    title_en = models.CharField(_("Title en"), max_length=250, null=True, blank=True)
    title_dech = models.CharField(_("Title dech"), max_length=250, null=True, blank=True)
    title_frch = models.CharField(_("Title frch"), max_length=250, null=True, blank=True)
    title_itch = models.CharField(_("Title itch"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_en"), FieldPanel("title_dech"),
        FieldPanel("title_frch"), FieldPanel("title_itch")
    ]

    api_fields = BasePage.api_fields + [
        APIField("title_en"), APIField("title_dech"),
        APIField("title_frch"), APIField("title_itch")
    ]

    parent_page_types = ["home.BlogIndexPage"]
    subpage_types = ["home.BlogDetailPage"]


class BlogDetailPage(BasePage):
    title_en = models.CharField(max_length=250, null=True, blank=True)
    title_dech = models.CharField(max_length=250, null=True, blank=True)
    title_frch = models.CharField(max_length=250, null=True, blank=True)
    title_itch = models.CharField(max_length=250, null=True, blank=True)

    thumbnail = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    body = StreamField(
        [
            ("title", TitleBlock()), ("banner_image", BannerImageBlock()),
            ("banner_video", BannerVideoBlock()),
            ("carousel", ImageCarouselBlock()), ("richtext", RichtextBlock()),
            ("faq", FaqBlock()), ("media_text", MediaTextBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    is_featured = models.BooleanField(default=False)
    tags_en = models.CharField(max_length=250, null=True, blank=True)
    tags_dech = models.CharField(max_length=250, null=True, blank=True)
    tags_frch = models.CharField(max_length=250, null=True, blank=True)
    tags_itch = models.CharField(max_length=250, null=True, blank=True)
    short_description_en = models.TextField(null=True, blank=True)
    short_description_dech = models.TextField(null=True, blank=True)
    short_description_frch = models.TextField(null=True, blank=True)
    short_description_itch = models.TextField(null=True, blank=True)

    @property
    def fetch_parent(self):
        obj = self.get_parent()
        return {
            "id": obj.specific.id,
            "title_en": getattr(obj.specific, "title_en", ""),
            "title_dech": getattr(obj.specific, "title_dech", ""),
            "title_frch": getattr(obj.specific, "title_frch", ""),
            "title_itch": getattr(obj.specific, "title_itch", ""),
            "slug": obj.specific.slug,
        }

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("title_en"), FieldPanel("title_dech"), FieldPanel("title_frch"), FieldPanel("title_itch"),
             FieldPanel("short_description_en"), FieldPanel("short_description_dech"),
             FieldPanel("short_description_frch"), FieldPanel("short_description_itch"),
             FieldPanel("is_featured"), FieldPanel("tags_en"), FieldPanel("tags_dech"),
             FieldPanel("tags_frch"), FieldPanel("tags_itch"), FieldPanel("thumbnail"),
             FieldPanel("body")],
            heading="Header"
        ),
        MultiFieldPanel([FieldPanel("author")], heading="Author"),
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("title_en"), APIField("title_dech"), APIField("title_frch"), APIField("title_itch"),
        APIField("short_description_en"), APIField("short_description_dech"),
        APIField("short_description_frch"), APIField("short_description_itch"),
        APIField("tags_en"), APIField("tags_dech"), APIField("tags_frch"), APIField("tags_itch"),
        APIField("thumbnail", serializer=ImageRenditionField({"original": "original|jpegquality-80|format-webp"})),
        APIField("author", serializer=AuthorSerializer()), APIField("last_published_at"),
        APIField("body"), APIField("is_featured"), APIField("fetch_parent")
    ]

    parent_page_types = ["home.BlogCategoryPage"]
    subpage_types = []


class PublicPage(BasePage):
    body = StreamField(
        [
            ("page_header", PageHeaderBlock()),
            ("title", TitleBlock()), ("richtext", RichtextBlock()),
            ("cta", CTABlock()), ("banner_image", BannerImageBlock()),
            ("banner_video", BannerVideoBlock()), ("carousel", ImageCarouselBlock()),
            ("faq", FaqBlock()), ("media_text", MediaTextBlock()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"), APIField("body")
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class AboutPage(BasePage):
    body = StreamField(
        [
            ("page_header", PageHeaderBlock()),
            ("title", TitleBlock()), ("cards", CardsListBlock()),
            ("stats", StatsBlock()), ("team", TeamBlock()), ("quote", QuoteBlock()),
            ("cta", CTABlock()), ("banner_video", BannerVideoBlock()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"), APIField("body")
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []



class ContactPage(BasePage):
    body = StreamField(
        [   
            ("page_header", PageHeaderBlock()), ("title", TitleBlock()),
            ("contact", ContactInfoBlock()),
            ("contact_form", ContactSection()), ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"), APIField("body")
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []