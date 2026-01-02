"""Module de tests pour les modèles de l'application lettings"""

from django.test import TestCase
from lettings.models import Address, Letting


class TestLettingsModels(TestCase):
    """Tests pour les modèles de l'application lettings"""

    def _create_address(self) -> Address:
        """Fonction utilitaire pour créer une adresse de test"""
        return Address.objects.create(
            number=1,
            street="Rue des Tests",
            city="Paris",
            state="FR",
            zip_code=75000,
            country_iso_code="FRA",
        )

    def test_address_str(self):
        """Vérifie que la méthode __str__ de Address retourne le format attendu"""
        address = self._create_address()
        self.assertEqual(str(address), "1 Rue des Tests")

    def test_letting_str(self):
        """Vérifie que la méthode __str__ de Letting retourne le format attendu"""
        address = self._create_address()
        letting = Letting.objects.create(title="Oceanview Retreat", address=address)
        self.assertEqual(str(letting), "Oceanview Retreat")

    def test_letting_has_one_to_one_address(self):
        """Vérifie que le modèle Letting a une relation OneToOne avec Address"""
        address = self._create_address()
        letting = Letting.objects.create(title="T1", address=address)
        self.assertEqual(letting.address, address)

    def test_sad_path_letting_has_one_to_one_address(self):
        """Vérifie que le modèle Letting ne peut pas partager une adresse (OneToOne)"""
        address = self._create_address()
        Letting.objects.create(title="T1", address=address)
        # Essaye de créer un deuxième Letting avec la même adresse
        with self.assertRaises(Exception):
            Letting.objects.create(title="T2", address=address)

    def test_check_plural(self):
        """Vérifie que la pluralisation se fait correctement"""
        self.assertEqual(Address._meta.verbose_name, "Address")
        self.assertEqual(Address._meta.verbose_name_plural, "Addresses")
        self.assertEqual(Letting._meta.verbose_name, "Letting")
        self.assertEqual(Letting._meta.verbose_name_plural, "Lettings")
