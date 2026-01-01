"""
Module de tests pour les URLs de l'application oc_lettings_site
Objectif que le routing est correct
"""

from django.test import TestCase
from django.urls import reverse, resolve
from oc_lettings_site import views


class TestOcLettingsUrls(TestCase):
    """Tests pour les URLs de l'application oc_lettings_site."""

    def test_home_url_resolves_index_view(self):
        """Vérifie que l'URL de la page d'accueil résout correctement vers la vue index."""
        homepage = resolve('/')
        self.assertEqual(homepage.func, views.index)

    def test_admin_url_resolves_admin_site(self):
        """Vérifie que l'URL de l'admin résout correctement vers l'interface d'administration."""
        admin_page = resolve('/admin/')
        # L'admin.site.urls ne peut pas être directement comparé comme une fonction,
        # donc on vérifie simplement que la résolution n'est pas None
        self.assertIn("admin", admin_page.func.__module__)

    def test_lettings_url_includes_lettings_urls(self):
        """Vérifie que l'URL des lettings inclut correctement les URLs de l'application lettings."""
        url = reverse('lettings:index')
        self.assertEqual(url, '/lettings/')

    def test_profiles_url_includes_profiles_urls(self):
        """Vérifie que l'URL des profiles inclut correctement les URLs de l'application profiles."""
        url = reverse('profiles:index')
        self.assertEqual(url, '/profiles/')

    def test_wrong_url_returns_404(self):
        """Vérifie qu'une URL non existante renvoie un code de statut 404."""
        response = self.client.get('/wrong-url/')
        self.assertEqual(response.status_code, 404)