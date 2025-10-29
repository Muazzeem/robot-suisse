from django.db import models
from django.utils.translation import gettext_lazy as _

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
    company_name_en = models.CharField(_("Company name en"), max_length=60)
    company_name_de_ch = models.CharField(_("Company name de ch"), max_length=60, null=True, blank=True)
    company_name_fr_ch = models.CharField(_("Company name fr ch"), max_length=60, null=True, blank=True)
    company_name_it_ch = models.CharField(_("Company name it ch"), max_length=60, null=True, blank=True)
    about_en = models.TextField(_("About en"), max_length=500)
    about_de_ch = models.TextField(_("About de ch"), max_length=500, null=True, blank=True)
    about_fr_ch = models.TextField(_("About fr ch"), max_length=500, null=True, blank=True)
    about_it_ch = models.TextField(_("About it ch"), max_length=500, null=True, blank=True)

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
    address1_en = models.CharField(_("Address 1 en"), max_length=100, null=True, blank=True)
    address1_de_ch = models.CharField(_("Address 1 de ch"), max_length=100, null=True, blank=True)
    address1_fr_ch = models.CharField(_("Address 1 fr ch"), max_length=100, null=True, blank=True)
    address1_it_ch = models.CharField(_("Address 1 it ch"), max_length=100, null=True, blank=True)

    address2_en = models.CharField(_("Address 2 en"), max_length=100, null=True, blank=True)
    address2_de_ch = models.CharField(_("Address 2 de ch"), max_length=100, null=True, blank=True)
    address2_fr_ch = models.CharField(_("Address 2 fr ch"), max_length=100, null=True, blank=True)
    address2_it_ch = models.CharField(_("Address 2 it ch"), max_length=100, null=True, blank=True)
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
                FieldPanel("company_name_en"),
                FieldPanel("company_name_de_ch"),
                FieldPanel("company_name_fr_ch"),
                FieldPanel("company_name_it_ch"),
                FieldPanel("about_en"),
                FieldPanel("about_de_ch"),
                FieldPanel("about_fr_ch"),
                FieldPanel("about_it_ch"),
                FieldPanel("logo"),
                FieldPanel("favicon"),
                FieldPanel("address1_en"),
                FieldPanel("address1_de_ch"),
                FieldPanel("address1_fr_ch"),
                FieldPanel("address1_it_ch"),
                FieldPanel("address2_en"),
                FieldPanel("address2_de_ch"),
                FieldPanel("address2_fr_ch"),
                FieldPanel("address2_it_ch"),
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


class MainMenuItem(models.Model):
    menu = ParentalKey("MainMenu", related_name="items", on_delete=models.CASCADE)
    name_en = models.CharField(_("Name en"), max_length=250)
    name_de_ch = models.CharField(_("Name de ch"), max_length=250, null=True, blank=True)
    name_fr_ch = models.CharField(_("Name fr ch"), max_length=250, null=True, blank=True)
    name_it_ch = models.CharField(_("Name it ch"), max_length=250, null=True, blank=True)
    link = models.CharField(_("Link"), max_length=250)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name_en"),
                FieldPanel("name_de_ch"),
                FieldPanel("name_fr_ch"),
                FieldPanel("name_it_ch"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
    ]

    def __str__(self):
        return self.name_en


class MainMenu(ClusterableModel):
    name_en = models.CharField(_("Name en"), max_length=250)
    name_de_ch = models.CharField(_("Name de ch"), max_length=250, null=True, blank=True)
    name_fr_ch = models.CharField(_("Name fr ch"), max_length=250, null=True, blank=True)
    name_it_ch = models.CharField(_("Name it ch"), max_length=250, null=True, blank=True)
    link = models.CharField(_("Link"), max_length=250, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name_en"),
                FieldPanel("name_de_ch"),
                FieldPanel("name_fr_ch"),
                FieldPanel("name_it_ch"),
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
        return self.name_en


class FooterMenuItem(models.Model):
    menu = ParentalKey("FooterMenu", related_name="items", on_delete=models.CASCADE)
    name_en = models.CharField(_("Name en"), max_length=250)
    name_de_ch = models.CharField(_("Name de ch"), max_length=250, null=True, blank=True)
    name_fr_ch = models.CharField(_("Name fr ch"), max_length=250, null=True, blank=True)
    name_it_ch = models.CharField(_("Name it ch"), max_length=250, null=True, blank=True)
    link = models.CharField(_("Link"), max_length=250)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name_en"),
                FieldPanel("name_de_ch"),
                FieldPanel("name_fr_ch"),
                FieldPanel("name_it_ch"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
    ]

    def __str__(self):
        return self.name_en


class FooterMenu(ClusterableModel):
    name_en = models.CharField(_("Name en"), max_length=250)
    name_de_ch = models.CharField(_("Name de ch"), max_length=250, null=True, blank=True)
    name_fr_ch = models.CharField(_("Name fr ch"), max_length=250, null=True, blank=True)
    name_it_ch = models.CharField(_("Name it ch"), max_length=250, null=True, blank=True)
    link = models.CharField(_("Link"), max_length=250, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name_en"),
                FieldPanel("name_de_ch"),
                FieldPanel("name_fr_ch"),
                FieldPanel("name_it_ch"),
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
        return self.name_en
