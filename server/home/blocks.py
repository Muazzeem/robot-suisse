from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class BannerBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        template = "home/blocks/banner_block.html"


class TwoImageBlock(blocks.StructBlock):
    image1 = ImageChooserBlock()
    image2 = ImageChooserBlock()

    class Meta:
        template = "home/blocks/two_image_block.html"


class RichtextBlock(blocks.RichTextBlock):
    class Meta:
        template = "home/blocks/richtext_block.html"


class FaqItemsBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock()


class FaqBlock(blocks.StructBlock):
    items = blocks.ListBlock(FaqItemsBlock())

    class Meta:
        template = "home/blocks/faq_block.html"
