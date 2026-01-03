"""
Module de tests pour les vues du site oc_lettings_site
Objectif : vérifier que la vue renvoie le bon template et le bon code de statut"""

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class TestsOcLettingsViews(TestCase):
    """Tests pour les vues de l'application oc_lettings_site."""
    def test_index_returns_200(self):
        """Vérifie que la vue index renvoie un code de statut 200."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_index_template(self):
        """Vérifie que la vue index utilise le template 'index.html'."""
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")

    def test_index_raises_when_render_fails(self):
        """Vérifie que la vue index lève une exception lorsque le rendu échoue."""
        with patch("oc_lettings_site.views.render", side_effect=Exception("crash")):
            with self.assertRaises(Exception):
                self.client.get(reverse("index"))