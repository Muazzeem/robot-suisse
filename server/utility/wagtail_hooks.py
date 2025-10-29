from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from .models import MainMenu, FooterMenu


class MainMenuAdmin(SnippetViewSet):
    model = MainMenu
    menu_label = "Main Menu"
    icon = "list-ul"
    list_display = ("name_en", "link")
    search_fields = ("name_em",)


class FooterMenuAdmin(SnippetViewSet):
    model = FooterMenu
    menu_label = "Footer Menu"
    icon = "list-ul"
    list_display = ("name_en", "link")
    search_fields = ("name_en",)


class MenuViewSetGroup(SnippetViewSetGroup):
    items = (MainMenuAdmin, FooterMenuAdmin)
    menu_icon = "list-ul"
    menu_label = "Menus"
    menu_order = 100

register_snippet(MenuViewSetGroup)