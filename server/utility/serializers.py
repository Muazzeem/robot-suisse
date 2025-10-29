from rest_framework import serializers
from .models import BasicSetting, SocialSetting, MainMenu, MainMenuItem, FooterMenu, FooterMenuItem


class BasicSettingSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()

    class Meta:
        model = BasicSetting
        fields = "__all__"

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.file.url
        return None

    def get_favicon(self, obj):
        if obj.favicon:
            return obj.favicon.file.url
        return None


class SocialSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialSetting
        fields = "__all__"


class MainMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMenuItem
        fields = "__all__"


class MainMenuSerializer(serializers.ModelSerializer):
    items = MainMenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MainMenu
        fields = ["id", "name_en", "name_de_ch", "name_fr_ch", "name_it_ch", "link", "items"]


class FooterMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterMenuItem
        fields = "__all__"


class FooterMenuSerializer(serializers.ModelSerializer):
    items = FooterMenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = FooterMenu
        fields = ["id", "name_en", "name_de_ch", "name_fr_ch", "name_it_ch", "link", "items"]
