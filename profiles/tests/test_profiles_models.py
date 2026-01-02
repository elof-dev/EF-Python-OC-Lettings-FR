"""Module de tests pour les modèles de l'application profiles"""

from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import Profile


class TestProfileModels(TestCase):
    """Tests pour les modèles de l'application profiles"""

    def test_str_returns_username(self):
        """Vérifie que la méthode __str__ retourne le nom d'utilisateur associé au profil"""
        user = User.objects.create_user(username="elodie", password="pwd")
        profile = Profile.objects.create(user=user, favorite_city="Lyon")
        self.assertEqual(str(profile), "elodie")

    def test_related_name_allows_user_profiles_profile(self):
        """Vérifie que le related_name permet d'accéder au profil depuis l'utilisateur"""
        user = User.objects.create_user(username="bob", password="pwd")
        profile = Profile.objects.create(user=user)
        self.assertEqual(user.profiles_profile, profile)

    def test_plural_names(self):
        """Vérifie que la pluralisation se fait correctement"""
        self.assertEqual(Profile._meta.verbose_name, "Profile")
        self.assertEqual(Profile._meta.verbose_name_plural, "Profiles")
