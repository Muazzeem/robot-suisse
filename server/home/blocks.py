from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleBlock(blocks.StructBlock):
    title_en = blocks.CharBlock(required=True, help_text="Main title for the banner")
    title_de_ch = blocks.CharBlock(required=True, help_text="Main title for the banner", blank=True, null=True)
    title_fr_ch = blocks.CharBlock(required=True, help_text="Main title for the banner", blank=True, null=True)
    title_it_ch = blocks.CharBlock(required=True, help_text="Main title for the banner", blank=True, null=True)
    subtitle_en = blocks.TextBlock(required=False, help_text="Optional subtitle or tagline")
    subtitle_de_ch = blocks.TextBlock(required=False, help_text="Optional subtitle or tagline", blank=True, null=True)
    subtitle_fr_ch = blocks.TextBlock(required=False, help_text="Optional subtitle or tagline", blank=True, null=True)
    subtitle_it_ch = blocks.TextBlock(required=False, help_text="Optional subtitle or tagline", blank=True, null=True)
    alignment = blocks.ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("center", "Center"),
            ("right", "Right"),
        ],
        default="left",
        required=True,
        help_text="Choose the text alignment"
    )

    class Meta:
        icon = "title"
        label = "Title Block"
        template = None

class BannerImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Upload an image for the banner")

    class Meta:
        icon = "media"
        label = "Banner Image Block"


class BannerVideoBlock(blocks.StructBlock):
    video_url = blocks.URLBlock(required=True, help_text="Enter a video URL for the banner")

    class Meta:
        icon = "media"
        label = "Banner Video Block"


class TwoImageBlock(blocks.StructBlock):
    title1_en = blocks.CharBlock(required=False, help_text="Title for the first image")
    title1_de_ch = blocks.CharBlock(required=False, help_text="Title for the first image", blank=True, null=True)
    title1_fr_ch = blocks.CharBlock(required=False, help_text="Title for the first image", blank=True, null=True)
    title1_it_ch = blocks.CharBlock(required=False, help_text="Title for the first image", blank=True, null=True)
    subtitle1_en = blocks.TextBlock(required=False, help_text="Subtitle for the first image")
    subtitle1_de_ch = blocks.TextBlock(required=False, help_text="Subtitle for the first image", blank=True, null=True)
    subtitle1_fr_ch = blocks.TextBlock(required=False, help_text="Subtitle for the first image", blank=True, null=True)
    subtitle1_it_ch = blocks.TextBlock(required=False, help_text="Subtitle for the first image", blank=True, null=True)
    image1 = ImageChooserBlock(required=True, help_text="First image")

    title2_en = blocks.CharBlock(required=False, help_text="Title for the second image")
    title2_de_ch = blocks.CharBlock(required=False, help_text="Title for the second image", blank=True, null=True)
    title2_fr_ch = blocks.CharBlock(required=False, help_text="Title for the second image", blank=True, null=True)
    title2_it_ch = blocks.CharBlock(required=False, help_text="Title for the second image", blank=True, null=True)
    subtitle2_en = blocks.TextBlock(required=False, help_text="Subtitle for the second image")
    subtitle2_de_ch = blocks.TextBlock(required=False, help_text="Subtitle for the second image", blank=True, null=True)
    subtitle2_fr_ch = blocks.TextBlock(required=False, help_text="Subtitle for the second image", blank=True, null=True)
    subtitle2_it_ch = blocks.TextBlock(required=False, help_text="Subtitle for the second image", blank=True, null=True)
    image2 = ImageChooserBlock(required=True, help_text="Second image")

    position = blocks.ChoiceBlock(
        choices=[
            ("top", "Image Top"),
            ("bottom", "Image Bottom"),
        ],
        default="top",
        required=True,
        help_text="Position of the image section"
    )

    class Meta:
        icon = "image"
        label = "Two Image Block"


class CarouselImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Carousel image")
    title_en = blocks.CharBlock(required=False, help_text="Optional title for this image")
    title_de_ch = blocks.CharBlock(required=False, help_text="Optional title for this image", blank=True, null=True)
    title_fr_ch = blocks.CharBlock(required=False, help_text="Optional title for this image", blank=True, null=True)
    title_it_ch = blocks.CharBlock(required=False, help_text="Optional title for this image", blank=True, null=True)
    extranal_link = blocks.CharBlock(required=False, help_text="Optional external link for this image")


    class Meta:
        icon = "image"
        label = "Carousel Image"


class ImageCarouselBlock(blocks.StructBlock):
    items = blocks.ListBlock(
        CarouselImageBlock(),
        help_text="Add one or more images with titles for the carousel"
    )

    class Meta:
        icon = "image"
        label = "Image Carousel Block"
        template = None


class RichtextBlock(blocks.RichTextBlock):
    class Meta:
        template = "home/blocks/richtext_block.html"


class FaqItemsBlock(blocks.StructBlock):
    question_en = blocks.CharBlock()
    question_de_ch = blocks.CharBlock(blank=True, null=True)
    question_fr_ch = blocks.CharBlock(blank=True, null=True)
    question_it_ch = blocks.CharBlock(blank=True, null=True)

    answer_en = blocks.RichTextBlock()
    answer_de_ch = blocks.RichTextBlock(blank=True, null=True)
    answer_fr_ch = blocks.RichTextBlock(blank=True, null=True)
    answer_it_ch = blocks.RichTextBlock(blank=True, null=True)


class FaqBlock(blocks.StructBlock):
    items = blocks.ListBlock(FaqItemsBlock())

    class Meta:
        template = "home/blocks/faq_block.html"


class MediaTextBlock(blocks.StructBlock):
    LAYOUT_CHOICES = [
        ("left_media", "Left media / Right text"),
        ("right_media", "Left text / Right media"),
    ]

    layout = blocks.ChoiceBlock(choices=LAYOUT_CHOICES, default="left_media", label="Layout")
    description_en = blocks.RichTextBlock()
    description_de_ch = blocks.RichTextBlock(blank=True, null=True)
    description_fr_ch = blocks.RichTextBlock(blank=True, null=True)
    description_it_ch = blocks.RichTextBlock(blank=True, null=True)

    media_type = blocks.ChoiceBlock(
        choices=[
            ("image", "Image"),
            ("video", "YouTube (URL)"),
        ],
        default="image",
        label="Media Type",
    )

    image = ImageChooserBlock(required=False)
    video_url = blocks.URLBlock(required=False, help_text="YouTube or any external video URL")

    button_text_en = blocks.CharBlock(required=False, max_length=50)
    button_text_de_ch = blocks.CharBlock(required=False, max_length=50, blank=True, null=True)
    button_text_fr_ch = blocks.CharBlock(required=False, max_length=50, blank=True, null=True)
    button_text_it_ch = blocks.CharBlock(required=False, max_length=50, blank=True, null=True)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        label = "Media + Text Section"
        template = None

from wagtail.contrib.table_block.blocks import TableBlock

class SpecificationBlock(blocks.StreamBlock):
    table_en = TableBlock(required=False)
    table_de_ch = TableBlock(required=False)
    table_fr_ch = TableBlock(required=False)
    table_it_ch = TableBlock(required=False)

    class Meta:
        icon = "list-ol"
        label = "Specification Block"
        template = None


COMMON_BLOCKS = [
    ("title", TitleBlock()),
    ("banner_image", BannerImageBlock()),
    ("banner_video", BannerVideoBlock()),
    ("two_images", TwoImageBlock()),
    ("carousel", ImageCarouselBlock()),
    ("richtext", RichtextBlock()),
    ("faq", FaqBlock()),
    ("media_text", MediaTextBlock()),
    ("specifications", SpecificationBlock()),
]
