from .models import MainMenu

def global_context(request):
    return {
        'main_menus': MainMenu.objects.filter().prefetch_related('items')
    }
