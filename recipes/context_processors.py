from django.conf import settings

def fonts(request):
    return {'SCRIPT_FONTS': settings.SCRIPT_FONTS}
