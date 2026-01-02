"""Module de tests pour les URLs de l'application lettings"""

from django.test import TestCase
from django.urls import resolve, reverse

from lettings import views


class TestLettingsUrls(TestCase):
    """Tests pour les URLs de l'application lettings"""

    def test_index_reverse(self):
        """Vérifie que la fonction reverse génère la bonne URL pour la page d'index"""
        index_url = reverse("lettings:index")
        self.assertEqual(index_url, "/lettings/")

    def test_letting_reverse(self):
        """Vérifie que la fonction reverse génère la bonne URL pour une page de letting"""
        letting_url = reverse("lettings:letting", kwargs={"letting_id": 1})
        self.assertEqual(letting_url, "/lettings/1/")

    def test_index_resolves_to_index_view(self):
        """Vérifie que la résolution de l'URL /lettings/ correspond à la vue index"""
        lettings_page = resolve("/lettings/")
        self.assertEqual(lettings_page.func, views.index)

    def test_letting_resolves_to_letting_view(self):
        """Vérifie que la résolution de l'URL /lettings/1/ correspond à la vue letting"""
        letting_page = resolve("/lettings/1/")
        self.assertEqual(letting_page.func, views.letting)

    def test_wrong_url_returns_404(self):
        """Vérifie qu'une URL non existante renvoie un code de statut 404"""
        response = self.client.get("/lettings/wrong-url/")
        self.assertEqual(response.status_code, 404)
