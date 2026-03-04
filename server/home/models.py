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
        "home.ProfilePage",
        "home.RobotIndexPage",
        "home.RobotPage",
        "home.BlogIndexPage",
        "home.ContactPage",
        "home.PublicPage",
        "home.BlogListPage",
        "home.CompanyPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["og_image"] = self.og_image
        return context

class ProfilePage(BasePage):
    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("title", TitleBlock()),
            ("spacer", SpacerBlock()),
            ("blog", BlogsBlock()), 
            ("stats", StatsBlock()),
            ("service_card", ServiceCardsSection()),
            ("companies", CompaniesBlock()),
            ("robots", RobotsBlock()),
            ("team", TeamBlock()),
            ("profile_contact", ProfileContactSection()),
            ("image", BannerImageBlock()),
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


# ---------------------------- Blog Pages ----------------------------
class BlogIndexPage(Page):
    tag = StreamField(
        [("tag", multi_lang_char(help_text="The tag for the page"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_title = StreamField(
        [("title", multi_lang_char(help_text="Hero title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_description = StreamField(
        [("description", multi_lang_richtext(required=False, help_text="Hero description"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    @property
    def categories(self):
        from .serializers import BlogCategoryPageSerializer
        childs = self.get_children()
        return BlogCategoryPageSerializer(childs, many=True).data

    content_panels = Page.content_panels + [
        FieldPanel("tag"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),
        FieldPanel("hero_image"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("categories"),
        APIField("hero_image"),
        APIField("tag"),
        APIField("hero_title"),
        APIField("hero_description"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.BlogCategoryPage"]


class BlogCategoryPage(BasePage):
    cat_title = StreamField(
        [("title", multi_lang_char(help_text="Category title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("cat_title")
    ]

    api_fields = BasePage.api_fields + [
        APIField("cat_title")
    ]

    parent_page_types = ["home.BlogIndexPage"]
    subpage_types = ["home.BlogDetailPage"]


class BlogDetailPage(BasePage):
    blog_title = StreamField(
        [("title", multi_lang_char(help_text="Blog title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    short_description = StreamField(
        [("description", multi_lang_richtext(required=False, help_text="Short description"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    tags = StreamField(
        [("tags", multi_lang_char(required=False, help_text="Blog tags"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    thumbnail = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    body = StreamField(
        [
            ("title", TitleBlock()),
            ("banner_image", BannerImageBlock()),
            ("banner_video", BannerVideoBlock()),
            ("carousel", ImageCarouselBlock()),
            ("richtext", RichtextBlock()),
            ("faq", FaqBlock()),
            ("media_text", MediaTextBlock())
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    is_featured = models.BooleanField(default=False)

    @property
    def fetch_parent(self):
        parent = self.get_parent().specific
        cat_title_value = {}
        if parent.cat_title:
            for block in parent.cat_title:
                cat_title_value[block.block_type] = block.value

        return {
            "id": parent.id,
            "title": cat_title_value,
            "slug": parent.slug,
        }

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("blog_title"),
                FieldPanel("short_description"),
                FieldPanel("is_featured"),
                FieldPanel("tags"),
                FieldPanel("thumbnail")
            ],
            heading="Header"
        ),
        MultiFieldPanel([FieldPanel("author")], heading="Author"),
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("blog_title"),
        APIField("short_description"),
        APIField("tags"),
        APIField("thumbnail", serializer=ImageRenditionField({"original": "original|jpegquality-80|format-webp"})),
        APIField("author", serializer=AuthorSerializer()),
        APIField("last_published_at"),
        APIField("body"),
        APIField("is_featured"),
        APIField("fetch_parent")
    ]

    parent_page_types = ["home.BlogCategoryPage"]
    subpage_types = []

# ---------------------------- Robot Pages ----------------------------

class RobotIndexPage(Page):
    tag = StreamField(
        [("tag", multi_lang_char(help_text="The tag for the page"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_title = StreamField(
        [("title", multi_lang_char(help_text="Hero title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_description = StreamField(
        [("description", multi_lang_richtext(required=False, help_text="Hero description"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    @property
    def categories(self):
        from .serializers import BlogCategoryPageSerializer
        childs = self.get_children()
        return BlogCategoryPageSerializer(childs, many=True).data

    content_panels = Page.content_panels + [
        FieldPanel("tag"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),
        FieldPanel("hero_image"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("categories"),
        APIField("hero_image"),
        APIField("tag"),
        APIField("hero_title"),
        APIField("hero_description"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.RobotCategoryPage"]

class RobotCategoryPage(BasePage):
    cat_title = StreamField(
        [("title", multi_lang_char(help_text="Category title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("cat_title")
    ]

    api_fields = BasePage.api_fields + [
        APIField("cat_title")
    ]

    parent_page_types = ["home.RobotIndexPage"]
    subpage_types = ["home.RobotDetailPage"]

class RobotDetailPage(BasePage):
    robot_title = StreamField(
        [("title", multi_lang_char(help_text="Robot title"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    short_description = StreamField(
        [("description", multi_lang_richtext(required=False, help_text="Short description"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    tags = StreamField(
        [("tags", multi_lang_char(required=False, help_text="Robot tags"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    body = StreamField(
        [
            ("title", TitleBlock()),
            ("banner_image", BannerImageBlock()),
            ("banner_video", BannerVideoBlock()),
            ("carousel", ImageCarouselBlock()),
            ("table", SpecificationBlock()),
            ("richtext", RichtextBlock()),
            ("faq", FaqBlock()),
            ("media_text", MediaTextBlock())
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    is_featured = models.BooleanField(default=False)

    @property
    def fetch_parent(self):
        parent = self.get_parent().specific

        cat_title_value = {}
        if parent.cat_title:
            for block in parent.cat_title:
                cat_title_value[block.block_type] = block.value

        return {
            "id": parent.id,
            "title": cat_title_value,
            "slug": parent.slug,
        }

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("robot_title"),
                FieldPanel("short_description"),
                FieldPanel("is_featured"),
                FieldPanel("tags"),
                FieldPanel("thumbnail")
            ],
            heading="Header"
        ),
        MultiFieldPanel([FieldPanel("author")], heading="Author"),
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("robot_title"),
        APIField("short_description"),
        APIField("tags"),
        APIField("thumbnail", serializer=ImageRenditionField({"original": "original|jpegquality-80|format-webp"})),
        APIField("author", serializer=AuthorSerializer()),
        APIField("last_published_at"),
        APIField("body"),
        APIField("is_featured"),
        APIField("fetch_parent")
    ]

    parent_page_types = ["home.RobotCategoryPage"]
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


class RobotPage(BasePage):
    body = StreamField(
        [
            ("page_header", PageHeaderBlock()),
            ("title", TitleBlock()),
            ("robots", RobotsFilterBlock()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
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
            ("how_it_works", HowItWorksBlock()), ("companies", CompaniesBlock()),
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


class BlogListPage(BasePage):
    body = StreamField(
        [   
            ("page_header", PageHeaderBlock()), ("title", TitleBlock()),
            ("blogs", BlogsListBlock()),
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

class CompanyPage(BasePage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.CompanyDetailPage"]

class CompanyDetailPage(BasePage):
    company_name = StreamField(
        [("name", multi_lang_char(help_text="Company name"))],
        use_json_field=True,
        blank=True,
        null=True,
    )
    logo = models.TextField(
        blank=True,
        help_text="URL of the company logo"
    )
    banner = models.TextField(
        blank=True,
        help_text="URL of the company banner"
    )


    short_description = StreamField(
        [("description", multi_lang_richtext(required=False, help_text="Short description"))],
        use_json_field=True,
        blank=True,
        null=True,
    )

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    body = StreamField(
        [
            ("company_header", CompanyHeaderBlock()),
            ("company_details", CompanyDetailsBlock()),
            ("contacts", ContactListBlock()),
            ("spacer", SpacerBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("company_name"),
                FieldPanel("short_description"),
                FieldPanel("cover_image"),
                FieldPanel("logo_image"),
                FieldPanel("logo"),
                FieldPanel("banner"),
            ],
            heading="Header"
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Body")
    ]

    api_fields = BasePage.api_fields + [
        APIField("company_name"),
        APIField("logo"),
        APIField("banner"),
        APIField("short_description"),
        APIField("cover_image", serializer=ImageRenditionField({"original": "original|jpegquality-80|format-webp"})),
        APIField("logo_image", serializer=ImageRenditionField({"original": "original|jpegquality-80|format-webp"})),
        APIField("body"),
    ]

    parent_page_types = [
        "home.CompanyPage",
    ]
    subpage_types = []

