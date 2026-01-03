"""Module de tests pour les vues de l'application profiles"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from profiles.models import Profile


class TestProfilesViews(TestCase):
    """Tests pour les vues de l'application profiles"""

    def test_index_returns_200_and_uses_template(self):
        """Vérifie que la vue index renvoie un code de statut 200 et utilise le bon template"""
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_index_context_contains_profiles_list(self):
        """Vérifie que le contexte de la vue index contient la liste des profils"""
        user = User.objects.create_user(username="elodie", password="pwd")
        profile = Profile.objects.create(user=user)

        response = self.client.get(reverse("profiles:index"))
        self.assertIn("profiles_list", response.context)
        self.assertIn(profile, response.context["profiles_list"])

    def test_profile_view_returns_200_and_uses_template(self):
        """Vérifie que la vue profile renvoie un code de statut 200 et utilise le bon template"""
        user = User.objects.create_user(username="elodie", password="pwd")
        profile = Profile.objects.create(user=user)

        response = self.client.get(
            reverse("profiles:profile", kwargs={"username": "elodie"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertEqual(response.context["profile"], profile)

    def test_profile_view_returns_404_when_user_unknown(self):
        """Vérifie que la vue profile renvoie statut code 404 lorsque l'utilisateur est inconnu"""
        response = self.client.get(
            reverse("profiles:profile", kwargs={"username": "unknown"})
        )
        self.assertEqual(response.status_code, 404)

    def test_index_raises_when_db_query_fails(self):
        """Vérifie que la vue index lève une exception lorsque la requête DB échoue"""
        with patch(
            "profiles.views.Profile.objects.all", side_effect=Exception("crash db")
        ):
            with self.assertRaises(Exception):
                self.client.get(reverse("profiles:index"))

    def test_profile_raises_on_unexpected_error(self):
        """Vérifie que la vue profile lève une exception lors d'une erreur inattendue"""
        with patch("profiles.views.get_object_or_404", side_effect=Exception("crash")):
            with self.assertRaises(Exception):
                self.client.get(
                    reverse("profiles:profile", kwargs={"username": "elodie"})
                )
