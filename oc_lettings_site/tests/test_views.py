"""
Module de tests pour les vues du site oc_lettings_site
Objectif : vérifier que la vue renvoie le bon template et le bon code de statut"""

from django.test import TestCase
from django.urls import reverse


class TestsOcLettingsViews(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_index_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")
