from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import BasicSetting, SocialSetting, MainMenu, FooterMenu
from .serializers import (
    BasicSettingSerializer,
    SocialSettingSerializer,
    MainMenuSerializer,
    FooterMenuSerializer,
)


class AllSettingsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        basic_setting = BasicSetting.objects.first()
        social_setting = SocialSetting.objects.first()

        main_menus = MainMenu.objects.all()
        footer_menus = FooterMenu.objects.all()

        data = {
            "basic_setting": BasicSettingSerializer(basic_setting).data if basic_setting else None,
            "social_setting": SocialSettingSerializer(social_setting).data if social_setting else None,
            "main_menus": MainMenuSerializer(main_menus, many=True).data,
            "footer_menus": FooterMenuSerializer(footer_menus, many=True).data,
        }

        return Response(data)
