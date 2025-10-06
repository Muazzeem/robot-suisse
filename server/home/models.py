from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField

from .choices import ROBOTS_CHOICES
from .forms import *
from . import blocks


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

    promote_panels = Page.promote_panels + [
        FieldPanel("og_image", help_text="size: width-1200px, height-630px"),
        FieldPanel("og_keywords"),
        FieldPanel("robots_directive"),
    ]

    class Meta:
        abstract = True


class HomePage(BasePage):
    template = "home/home.html"

    parent_page_types = []
    subpage_types = ["ContactPage", "ServiceListPage", "ServicePage", "AboutUsPage", "PrivacyPage", "TermsPage", "RegistrationPage"]


class ContactPage(BasePage):
    template = "home/contact.html"

    parent_page_types = ["HomePage"]
    subpage_types = []


class ServicePage(BasePage):
    template = "home/services.html"

    parent_page_types = ["HomePage"]
    subpage_types = [
        "ServiceDetailPage",
    ]


class ServiceDetailPage(BasePage):
    template = "home/service_detail.html"

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Cover Image"),
        help_text=_("Cover image for the service detail page")
    )

    body = StreamField(
        [
            ("banner_block", blocks.BannerBlock()),
            ("richtext_block", blocks.RichtextBlock()),
            ("two_image_block", blocks.TwoImageBlock()),
            ("faq_block", blocks.FaqBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    parent_page_types = ["ServicePage"]
    subpage_types = []


class AboutUsPage(BasePage):
    template = "home/about_us.html"

    parent_page_types = ["HomePage"]
    subpage_types = []


class PublicPage(BasePage):
    template = "home/public.html"

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Cover Image"),
        help_text=_("Cover image for the service detail page")
    )

    body = StreamField(
        [
            ("banner_block", blocks.BannerBlock()),
            ("richtext_block", blocks.RichtextBlock()),
            ("two_image_block", blocks.TwoImageBlock()),
            ("faq_block", blocks.FaqBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    parent_page_types = ["HomePage"]
    subpage_types = []


class RegistrationPage(Page):
    template = "home/service-registration.html"

    parent_page_types = ["HomePage"]
    subpage_types = []

