from .models import GeneralSettings


def general_settings(request):
    return {"general": GeneralSettings.get()}
