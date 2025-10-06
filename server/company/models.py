from django.db import models
from core.models import BasePage
from home.serializers import BlogCategoryPageSerializer
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from django.utils.translation import gettext_lazy as _



class CompanySocialLink(Orderable):
    company = ParentalKey("CompanyDetailsPage", related_name="social_links", on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, help_text="e.g. LinkedIn, X, Facebook")
    url = models.URLField()

    panels = [
        FieldPanel("platform"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return f"{self.platform}: {self.url}"
    
    
class CompanyIndexPage(BasePage):
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
        "CompanyCategoryPage",
    ]


class CompanyDetailsPage(BasePage):
    """
    Represents a company with manually entered multilingual fields.
    """

    COMPANY_TYPE_CHOICES = [
        ("manufacturer", _("Manufacturer")),
        ("integrator", _("Integrator")),
        ("distributor", _("Distributor")),
        ("supplier", _("Supplier")),
        ("service_provider", _("Service Provider")),
        ("other", _("Other")),
    ]

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("inactive", _("Inactive")),
        ("pending", _("Pending")),
    ]

    name_en = models.CharField(max_length=255, verbose_name=_("Name (English)"))
    name_de_ch = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (German - Switzerland)"))
    name_fr_ch = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French - Switzerland)"))
    name_it_ch = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (Italian - Switzerland)"))

    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES, verbose_name=_("Company Type"))

    description_en = RichTextField(blank=True, verbose_name=_("Description (English)"))
    description_de_ch = RichTextField(blank=True, verbose_name=_("Description (German - Switzerland)"))
    description_fr_ch = RichTextField(blank=True, verbose_name=_("Description (French - Switzerland)"))
    description_it_ch = RichTextField(blank=True, verbose_name=_("Description (Italian - Switzerland)"))

    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
    )
    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Banner"),
    )
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    industries = models.JSONField(blank=True, null=True, verbose_name=_("Industries"))
    certifications = models.JSONField(blank=True, null=True, verbose_name=_("Certifications"))
    locations = models.JSONField(blank=True, null=True, verbose_name=_("Branch Locations"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name=_("Status"))

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("name_en"),
                FieldPanel("name_de_ch"),
                FieldPanel("name_fr_ch"),
                FieldPanel("name_it_ch"),
                FieldPanel("company_type"),
                FieldPanel("status"),
                
            ],
            heading=_("Basic Information (Multilingual)"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("country"),
                FieldPanel("city"),
                FieldPanel("website"),
            ],
            heading=_("Location & Contact"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("banner"),
            ],
            heading=_("Media"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("description_en"),
                FieldPanel("description_de_ch"),
                FieldPanel("description_fr_ch"),
                FieldPanel("description_it_ch"),
            ],
            heading=_("Descriptions (Multilingual)"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("industries"),
                FieldPanel("certifications"),
                FieldPanel("locations"),
            ],
            heading=_("Additional Info"),
        ),
        # MultiFieldPanel(
        #     [
        #         InlinePanel("social_links", label="Social Links"),
        #     ],
        #     heading="Social Media",
        # ),
    ]

    parent_page_types = ["company.CompanyCategoryPage"]
    subpage_types = []

    api_fields = BasePage.api_fields + [
        APIField("name_en"),
        APIField("name_de_ch"),
        APIField("name_fr_ch"),
        APIField("name_it_ch"),
        APIField("company_type"),
        APIField("description_en"),
        APIField("description_de_ch"),
        APIField("description_fr_ch"),
        APIField("description_it_ch"),
        APIField("country"),
        APIField("city"),
        APIField("website"),
        APIField("logo"),
        APIField("banner"),
        APIField("industries"),
        APIField("certifications"),
        APIField("locations"),
        APIField("status"),
    ]

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class CompanyCategoryPage(BasePage):
    title_ar = models.CharField(_("Title ar"), max_length=250, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
    ]

    api_fields = BasePage.api_fields + [APIField("title"), APIField("title_ar")]

    parent_page_types = [
        "CompanyIndexPage",
    ]
    subpage_types = [
        "CompanyDetailsPage",
    ]
