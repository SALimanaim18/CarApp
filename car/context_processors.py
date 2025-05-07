# This file is needed for  passing variable to base.html
from .models import Car, Privacy, Ads


def ad_processor(request):
    popup_ads = Ads.objects.all()
    ad = None  # Valeur par défaut si la liste est vide
    if popup_ads:
        ad = popup_ads[0]
    return {
        'ad': ad
    }