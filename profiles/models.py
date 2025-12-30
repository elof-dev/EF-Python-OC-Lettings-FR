from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Modèle représentant un profil utilisateur"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profiles_profile"
    )
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Représentation en chaîne de caractères du profil
        utilisé dans l'admin Django"""
        return self.user.username

    class Meta:
        """Meta données pour le modèle Profile"""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
