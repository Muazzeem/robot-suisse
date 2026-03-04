from django.db import models
from django.utils.text import slugify

class ContactPerson(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.name


class Company(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    source_page = models.IntegerField(default=0)
    is_detail_fetched = models.BooleanField(default=False)
    last_updated = models.DateTimeField()
    banner_image = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    detail_country = models.CharField(max_length=255, blank=True, null=True)
    detail_type = models.CharField(max_length=100, blank=True, null=True)
    detail_employees = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_persons = models.ManyToManyField(ContactPerson, related_name="organizations", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"
