from django.shortcuts import render, get_object_or_404
from .models import Profile
import logging
from django.http import Http404

logger = logging.getLogger(__name__)


# Sed placerat quam in pulvinar commodo. Nullam laoreet consectetur ex, sed consequat libero
# pulvinar eget. Fusc faucibus, urna quis auctor pharetra, massa dolor cursus neque, quis dictum
# lacus d
def index(request):
    """
    Affiche la liste des profils utilisateurs
    Récupère tous les objets Profile depuis la db,
    les place dans le contexte sous la clé 'profiles_list',
    et rend le template 'profiles/index.html' avec ce contexte.
    """
    try:
        profiles_list = Profile.objects.all()
        context = {"profiles_list": profiles_list}
        return render(request, "profiles/index.html", context)
    except Exception:
        logger.exception("Erreur lors du rendu de la page d'accueil des profils")
        raise


# Aliquam sed metus eget nisi tincidunt ornare accumsan eget lac laoreet neque quis, pellentesque
# dui. Nullam facilisis pharetra vulputate. Sed tincidunt, dolor id facilisis fringilla, eros leo
# tristique lacus, it. Nam aliquam dignissim congue. Pellentesque habitant morbi tristique senectus
# et netus et males
def profile(request, username):
    """
    Affiche les détails d'un profil utilisateur spécifique.
    Récupère l'objet Profile correspondant au nom d'utilisateur fourni,
    le place dans le contexte sous la clé 'profile',
    Rend le template 'profiles/profile.html'.
    """
    try:
        profile_obj = get_object_or_404(Profile, user__username=username)
    except Http404:
        logger.warning("Profil non trouvé", extra={"username": username})
        raise
    except Exception:
        logger.exception(
            "Erreur inattendue lors du chargement du profil",
            extra={"username": username},
        )
        raise

    context = {"profile": profile_obj}
    return render(request, "profiles/profile.html", context)
