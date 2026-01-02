"""Module de tests pour les URLs de l'application profiles"""

from django.test import TestCase
from django.urls import resolve, reverse

from profiles import views


class TestProfilesUrls(TestCase):
    """Tests pour les URLs de l'application profiles"""

    def test_index_reverse(self):
        """Vérifie que la fonction reverse génère la bonne URL pour la page d'index"""
        index_url = reverse("profiles:index")
        self.assertEqual(index_url, "/profiles/")

    def test_profile_reverse(self):
        """Vérifie que la fonction reverse génère la bonne URL pour la page de profil"""
        profile_url = reverse("profiles:profile", kwargs={"username": "HeadlinesGazer"})
        self.assertEqual(profile_url, "/profiles/HeadlinesGazer/")

    def test_index_resolves_to_index_view(self):
        """Vérifie que la résolution de l'URL /profiles/ correspond à la vue index"""
        profiles_page = resolve("/profiles/")
        self.assertEqual(profiles_page.func, views.index)

    def test_profile_resolves_to_profile_view(self):
        """Vérifie la résolution de l'URL /profiles/HeadlinesGazer/ correspond à la vue profile"""
        profile_page = resolve("/profiles/HeadlinesGazer/")
        self.assertEqual(profile_page.func, views.profile)

    def test_wrong_url_returns_404(self):
        """Vérifie qu'une URL non existante renvoie un code de statut 404"""
        response = self.client.get("/profiles/wrong-url/")
        self.assertEqual(response.status_code, 404)
