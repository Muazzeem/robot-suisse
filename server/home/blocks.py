import os
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

# -----------------------------
# Reusable Blocks / Helpers
# -----------------------------

class ImageChooserBlock(DefaultImageChooserBlock):
    """Custom Image Chooser with WebP rendition for non-GIF images."""
    def get_api_representation(self, value, context=None):
        if not value:
            return None
        ext = os.path.splitext(value.file.name)[1].lower()
        if ext == ".gif":
            data = {
                "id": value.id,
                "title": value.title,
                "original": {
                    "src": value.file.url,
                    "width": value.width,
                    "height": value.height,
                    "alt": value.title,
                },
            }
        else:
            rendition = value.get_rendition("original|jpegquality-80|format-webp")
            data = {
                "id": value.id,
                "title": value.title,
                "original": rendition.attrs_dict,
            }

        rules = getattr(self.meta, "rendition_rules", {})
        for name, rule in (rules or {}).items():
            data[name] = value.get_rendition(rule).attrs_dict

        return data

def multi_lang_char(required=True, help_text=""):
    return blocks.StructBlock([
        ("en", blocks.CharBlock(required=required, help_text=help_text + " (EN)")),
        ("dech", blocks.CharBlock(required=False, help_text=help_text + " (DE)")),
        ("frch", blocks.CharBlock(required=False, help_text=help_text + " (FR)")),
        ("itch", blocks.CharBlock(required=False, help_text=help_text + " (IT)")),
    ])

def multi_lang_richtext(required=True, help_text=""):
    return blocks.StructBlock([
        ("en", blocks.RichTextBlock(required=required, help_text=help_text + " (EN)")),
        ("dech", blocks.RichTextBlock(required=False, help_text=help_text + " (DE)")),
        ("frch", blocks.RichTextBlock(required=False, help_text=help_text + " (FR)")),
        ("itch", blocks.RichTextBlock(required=False, help_text=help_text + " (IT)")),
    ])

class HeroSubItemBlock(blocks.StructBlock):
    title = multi_lang_char()

class HeroTitleBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = multi_lang_char()
    subtitle = multi_lang_richtext(required=False)
    sub_items = blocks.ListBlock(HeroSubItemBlock())

    class Meta:
        icon = "title"
        label = "Hero Title Block"

class TitleBlock(blocks.StructBlock):
    bg_color_code = blocks.CharBlock(required=False)
    tag = multi_lang_char()
    title = multi_lang_richtext()
    alignment = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("center", "Center"), ("right", "Right")],
        default="left",
        required=True
    )

    class Meta:
        icon = "title"
        label = "Title Block"

class HeaderButtonsBlock(blocks.StructBlock):
    text = multi_lang_char(required=False)
    link = blocks.CharBlock(required=False)

    class Meta:
        icon = "link"
        label = "Header Button Block"

class PageHeaderBlock(blocks.StructBlock):
    tag = multi_lang_char(required=False)
    hero_title = multi_lang_char()
    hero_subtitle = multi_lang_richtext(required=False)
    image = ImageChooserBlock()
    buttons = blocks.ListBlock(HeaderButtonsBlock())

    class Meta:
        icon = "image"
        label = "Page Header Block"

class MediaTextBlock(blocks.StructBlock):
    layout = blocks.ChoiceBlock(
        choices=[("left_media", "Left media / Right text"), ("right_media", "Left text / Right media")],
        default="left_media"
    )
    description = multi_lang_richtext()
    media_type = blocks.ChoiceBlock(choices=[("image", "Image"), ("video", "YouTube (URL)")], default="image")
    image = ImageChooserBlock(required=False)
    video_url = blocks.URLBlock(required=False)
    button_text = multi_lang_char(required=False)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        label = "Media + Text Section"

class CardsBlock(blocks.StructBlock):
    icon = blocks.CharBlock(required=False)
    description = multi_lang_richtext()
    
    class Meta:
        icon = "image"
        label = "Cards Block"

class StatsBlock(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock([
            ("description", multi_lang_richtext())
        ])
    )

    class Meta:
        icon = "image"
        label = "Stats Block"

class FaqBlock(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock([
            ("question", multi_lang_char()),
            ("answer", multi_lang_richtext())
        ])
    )

    class Meta:
        icon = "help"
        label = "FAQ Block"

class TabItemBlock(blocks.StructBlock):
    title = multi_lang_char()
    content = multi_lang_richtext()
    icon = blocks.CharBlock(required=False)
    button_text = multi_lang_char(required=False)
    button_link = blocks.CharBlock(required=False)
    image = ImageChooserBlock(required=False)

class TabsBlock(blocks.StructBlock):
    items = blocks.ListBlock(TabItemBlock())

    class Meta:
        icon = "image"
        label = "Tabs Block"

class BannerImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    class Meta:
        icon = "image"
        label = "Banner Image Block"

class BannerVideoBlock(blocks.StructBlock):
    video_url = blocks.URLBlock(required=True)
    class Meta:
        icon = "media"
        label = "Banner Video Block"

class SpecificationBlock(blocks.StructBlock):
    table = blocks.StructBlock([
        ("en", TableBlock(required=False)),
        ("dech", TableBlock(required=False)),
        ("frch", TableBlock(required=False)),
        ("itch", TableBlock(required=False)),
    ])
    class Meta:
        icon = "list-ol"
        label = "Specification Block"

class CategoryCardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("icon", blocks.CharBlock(required=False)),
            ("description", multi_lang_richtext(required=False)),
        ])
    )

    class Meta:
        icon = "placeholder"
        label = "Cards with Icons"

class FeaturesBlock(blocks.StructBlock):
    title = multi_lang_char()
    features = blocks.ListBlock(
        blocks.StructBlock([
            ("icon", blocks.CharBlock(required=False)),
            ("title", multi_lang_char()),
            ("description", multi_lang_richtext(required=False)),
        ])
    )

    class Meta:
        icon = "placeholder"
        label = "Features Block"

class RobotsBlock(blocks.StructBlock):
    class Meta:
        icon = "cogs"
        label = "Robots Block"

class CTABlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    subtitle = multi_lang_richtext(required=False)
    button_text = multi_lang_char(required=False)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = "link"
        label = "CTA Block"

class CategoriesBlock(blocks.StructBlock):
    categories = blocks.ListBlock(
        blocks.StructBlock([
            ("image", ImageChooserBlock(required=False)),
            ("description", multi_lang_richtext(required=False))
        ])
    )

    class Meta:
        icon = "list-ul"
        label = "Categories Block"

class BlogsBlock(blocks.StructBlock):
    class Meta:
        icon = "doc-full"
        label = "Blogs Block"

class ChatBlock(blocks.StructBlock):
    details = multi_lang_richtext(required=False)
    button_text = multi_lang_char(required=False)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = "user"
        label = "Chat Block"

class ContactSection(blocks.StructBlock):
    description = multi_lang_richtext(required=False)
    icon = blocks.CharBlock(required=False)
    chat_section = multi_lang_richtext(required=False)
    button_text = multi_lang_char(required=False)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = "form"
        label = "Contact Section"

class SpacerBlock(blocks.StructBlock):
    height = blocks.IntegerBlock(default=20, help_text="Height in rem")

    class Meta:
        icon = "arrows-up-down"
        label = "Spacer Block"


class ImageCarouselBlock(blocks.StructBlock):
    images = blocks.ListBlock(
        ImageChooserBlock()
    )
    class Meta:
        icon = "image"
        label = "Image Carousel Block"

class RichtextBlock(blocks.StructBlock):
    content = multi_lang_richtext(required=False)
    class Meta:
        icon = "doc-full"
        label = "Richtext Block"

class CardsListBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        CardsBlock()
    )

    class Meta:
        icon = "image"
        label = "Cards List"

class TeamBlock(blocks.StructBlock):
    team = CategoriesBlock()

    class Meta:
        icon = "image"
        label = "Team Block"

class QuoteBlock(blocks.StructBlock):
    quote = multi_lang_richtext(required=False)
    author = multi_lang_char(required=False)

    class Meta:
        icon = "image"
        label = "Quote Block"

class ContactInfoBlock(blocks.StructBlock):

    class Meta:
        icon = "image"
        label = "Contact Info"