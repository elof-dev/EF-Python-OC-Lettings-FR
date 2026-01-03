from django.shortcuts import render, get_object_or_404
from .models import Letting
import logging
from django.http import Http404


logger = logging.getLogger(__name__)


# Aenean leo magna, vestibulum et tincidunt fermentum, consectetur quis velit. Sed non placerat
# massa. Integer est nunc, pulvinar a tempor et, bibendum id arcu. Vestibulum ante ipsum primis in
# faucibus orci luctus et ultrices posuere cubilia curae; Cras eget scelerisque
def index(request):
    """
    Affiche la page d'accueil du site de lettings.
    Récupère tous les objets Letting depuis la db,
    les place dans le contexte sous la clé 'lettings_list',
    Rend le template 'index.html'.
    """
    try:
        lettings_list = Letting.objects.all()
        context = {"lettings_list": lettings_list}
        return render(request, "lettings/index.html", context)
    except Exception:
        logger.exception("Erreur lors du rendu de la page d'accueil des lettings")
        raise


# Cras ultricies dignissim purus, vitae hendrerit ex varius non. In accumsan porta nisl id
#  eleifend. Praesent dignissim, odio eu consequat pretium, purus urna vulputate arcu, vitae
# efficitur lacus justo nec purus. Aenean finibus faucibus lectus at porta. Maecenas auctor, est ut
# luctus congue, dui enim mattis enim, ac condimentum velit libero in magna. Suspendisse potenti.
# In tempus a nisi sed laoreet. Suspendisse porta dui eget sem accumsan interdum. Ut quis urna
# pellentesque justo mattis ullamcorper ac non tellus. In tristique mauris eu velit fermentum,
# tempus pharetra est luctus. Vivamus consequat aliquam libero, eget bibendum lorem. Sed non dolor
# risus. Mauris condimentum auctor elementum. Donec quis nisi ligula. Integer vehicula tincidunt
# enim, ac lacinia augue pulvinar sit amet.
def letting(request, letting_id):
    """
    Affiche les détails d'un letting spécifique.
    Récupère l'objet Letting correspondant à l'ID fourni,
    le place dans le contexte sous la clé 'letting',
    Rend le template 'letting.html'.
    """
    try:
        letting_obj = get_object_or_404(Letting, id=letting_id)
    except Http404:
        logger.warning("Letting not found", extra={"letting_id": letting_id})
        raise
    except Exception:
        logger.exception(
            "Erreur lors du chargement du letting", extra={"letting_id": letting_id}
        )
        raise

    context = {"title": letting_obj.title, "address": letting_obj.address}
    return render(request, "lettings/letting.html", context)
