from wagtail.snippets.views.snippets import (
    SnippetViewSet,
    SnippetViewSetGroup,
)
from wagtail.snippets.models import register_snippet

from .models import *


class ContactUsAdmin(SnippetViewSet):
    model = ContactUs
    menu_label = "Contact Us"
    icon = "folder"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("full_name", "email", "phone", "get_status_display")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("status",)


class HelpViewSetGroup(SnippetViewSetGroup):
    items = (ContactUsAdmin,)
    menu_icon = "folder"
    menu_label = "Help"
    menu_name = "Help"


register_snippet(HelpViewSetGroup)


class MainMenuAdmin(SnippetViewSet):
    model = MainMenu
    menu_label = "Main Menu"
    icon = "folder"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "link")
    search_fields = ("name",)


class FooterMenuAdmin(SnippetViewSet):
    model = FooterMenu
    menu_label = "Footer Menu"
    icon = "folder"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "link")
    search_fields = ("name",)


class MenuViewSetGroup(SnippetViewSetGroup):
    items = (MainMenuAdmin, FooterMenuAdmin)
    menu_icon = "folder"
    menu_label = "Menus"
    menu_name = "Menus"


register_snippet(MenuViewSetGroup)

