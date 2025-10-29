from django.db import models


class ContactUsStatusChoice(models.IntegerChoices):
    UNSEEN = 1, "Unseen"
    SEEN = 2, "Seen"
