from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from .choices import *


@register_setting
class BasicSetting(BaseGenericSetting):
    company_name = models.CharField(_("Company name"), max_length=60)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    address1 = models.CharField(_("Address 1"), max_length=100, null=True, blank=True)
    address2 = models.CharField(_("Address 2"), max_length=100, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=100, null=True, blank=True)
    t_c = models.URLField(
        _("Terms & condition link"), max_length=150, null=True, blank=True
    )
    privacy_policy = models.URLField(
        _("Privacy policy link"), max_length=150, null=True, blank=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("company_name"),
                FieldPanel("logo"),
                FieldPanel("favicon"),
                FieldPanel("address1"),
                FieldPanel("address2"),
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("t_c"),
                FieldPanel("privacy_policy"),
            ],
            heading="Basic",
        ),
    ]


@register_setting
class SocialSetting(BaseGenericSetting):
    fb = models.CharField(_("Facebook"), max_length=260, null=True, blank=True)
    instagram = models.CharField(_("Instagram"), max_length=260, null=True, blank=True)
    linkedin = models.CharField(_("Linkedin"), max_length=260, null=True, blank=True)
    whatsapp = models.CharField(_("WhatsApp"), max_length=260, null=True, blank=True)
    x = models.CharField(_("X"), max_length=260, null=True, blank=True)
    youtube = models.CharField(_("Youtube"), max_length=260, null=True, blank=True)
    tiktok = models.CharField(_("Tiktok"), max_length=260, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("fb"),
                FieldPanel("instagram"),
                FieldPanel("linkedin"),
                FieldPanel("whatsapp"),
                FieldPanel("x"),
                FieldPanel("youtube"),
                FieldPanel("tiktok"),
            ],
            heading="Basic",
        ),
    ]


class ContactUs(models.Model):
    full_name = models.CharField(_("Full name"), max_length=150)
    email = models.EmailField(_("Email"), max_length=254)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)
    message = models.TextField(_("Message"), max_length=500)
    status = models.IntegerField(
        _("Status"),
        choices=ContactUsStatusChoice.choices,
        default=ContactUsStatusChoice.UNSEEN,
    )
    creation_time = models.DateTimeField(
        _("Creation time"), auto_now_add=True, null=True, blank=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("full_name"),
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("message"),
                FieldPanel("status"),
            ],
            heading="Basic",
        ),
    ]


class Service(models.Model):
    title = models.CharField(_("Title"), max_length=250)
    subtitle = models.CharField(_("Title"), max_length=250, null=True, blank=True)
    icon_image = models.CharField(
        _("Icon image"), max_length=250, null=True, blank=True
    )
    detail_page_link = models.CharField(
        _("Link"), max_length=250, null=True, blank=True
    )
    description = models.TextField(_("Description"), null=True, blank=True)
    service_cover = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("description"),
                FieldPanel("icon_image"),
                FieldPanel("service_cover"),
                FieldPanel("detail_page_link"),
            ],
            heading="Basic",
        ),
    ]


class MainMenuItem(models.Model):
    menu = ParentalKey("MainMenu", related_name="items", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=250)
    link = models.CharField(_("Link"), max_length=250)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
    ]

    def __str__(self):
        return self.name


class MainMenu(ClusterableModel):
    name = models.CharField(_("Name"), max_length=250)
    link = models.CharField(_("Link"), max_length=250, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
        MultiFieldPanel(
            [
                InlinePanel("items"),
            ],
            heading="Items",
        ),
    ]

    def __str__(self):
        return self.name


class FooterMenuItem(models.Model):
    menu = ParentalKey("FooterMenu", related_name="items", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=250)
    link = models.CharField(_("Link"), max_length=250)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
    ]

    def __str__(self):
        return self.name


class FooterMenu(ClusterableModel):
    name = models.CharField(_("Name"), max_length=250)
    link = models.CharField(_("Link"), max_length=250, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
        MultiFieldPanel(
            [
                InlinePanel("items"),
            ],
            heading="Items",
        ),
    ]

    def __str__(self):
        return self.name


class Subscribe(models.Model):
    email = models.EmailField(
        _("Email"), max_length=254, null=True, blank=True
    )

    def __str__(self):
        return self.email
