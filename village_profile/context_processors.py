"""
Context Processors untuk Village Profile
Menyediakan data village profile ke semua template
"""

from .models import VillageProfile


def village_profile(request):
    """
    Menambahkan data village profile ke context
    Termasuk logo desa, nama desa, dll
    """
    try:
        profile = VillageProfile.objects.filter(is_active=True).first()
        return {
            'village_profile': profile,
        }
    except Exception as e:
        return {
            'village_profile': None,
        }

