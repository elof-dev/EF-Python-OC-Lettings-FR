"""Module de tests pour les vues de l'application lettings"""

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from lettings.models import Address, Letting


class TestLettingsViews(TestCase):
    """Tests pour les vues de l'application lettings"""

    def _create_letting(self) -> Letting:
        """Fonction utilitaire pour créer un objet Letting avec une adresse associée"""
        address = Address.objects.create(
            number=1,
            street="Rue des Tests",
            city="Paris",
            state="FR",
            zip_code=75000,
            country_iso_code="FRA",
        )
        return Letting.objects.create(title="Nice place Test", address=address)

    def test_index_returns_200_and_uses_template(self):
        """Vérifie que la vue index renvoie un code de statut 200 et utilise le bon template"""
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_index_context_contains_lettings_list(self):
        """Vérifie que le contexte de la vue index contient la liste des lettings"""
        letting = self._create_letting()

        response = self.client.get(reverse("lettings:index"))
        self.assertIn("lettings_list", response.context)
        self.assertIn(letting, response.context["lettings_list"])

    def test_letting_view_returns_200_and_uses_template(self):
        """Vérifie que la vue letting renvoie un code de statut 200 et utilise le bon template"""
        letting = self._create_letting()

        response = self.client.get(
            reverse("lettings:letting", kwargs={"letting_id": letting.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/letting.html")
        self.assertEqual(response.context["title"], letting.title)
        self.assertEqual(response.context["address"], letting.address)

    def test_letting_view_returns_404_when_unknown(self):
        """Vérifie que la vue letting renvoie un statut code 404 lorsque le letting est inconnu"""
        response = self.client.get(
            reverse("lettings:letting", kwargs={"letting_id": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_index_raises_when_db_query_fails(self):
        """Vérifie que la vue index lève une exception lorsque la requête DB échoue"""
        with patch(
            "lettings.views.Letting.objects.all", side_effect=Exception("crash db")
        ):
            with self.assertRaises(Exception):
                self.client.get(reverse("lettings:index"))

    def test_letting_raises_on_unexpected_error(self):
        """Vérifie que la vue letting lève une exception lors d'une erreur inattendue"""
        with patch("lettings.views.get_object_or_404", side_effect=Exception("crash")):
            with self.assertRaises(Exception):
                self.client.get(reverse("lettings:letting", kwargs={"letting_id": 1}))
