from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models


class Address(models.Model):
    """Modèle représentant une adresse"""

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)]
    )

    def __str__(self):
        """Représentation en chaîne de caractères de l'adresse
        utilisé dans l'admin Django"""
        return f"{self.number} {self.street}"

    class Meta:
        """Meta données pour le modèle Address"""

        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Letting(models.Model):
    """Modèle représentant un letting"""

    title = models.CharField(max_length=256)
    # Relation OneToOne avec le modèle Address : donc 1 letting a 1 adresse
    # Si un jour on veut réutiliser une adresse pour plusieurs lettings,
    # il faudra changer ce champ en ForeignKey
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Représentation en chaîne de caractères du letting
        utilisé dans l'admin Django"""
        return self.title

    class Meta:
        """Meta données pour le modèle Letting"""

        verbose_name = "Letting"
        verbose_name_plural = "Lettings"
