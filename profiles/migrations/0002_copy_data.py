from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """Fonction qui copie les données de l'ancien modèle Profile vers le nouveau modèle Profile."""
    # Récupération des modèles des deux applications
    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")
    # Pour chaque ancien profil, on crée un nouveau profil
    for old_profile in OldProfile.objects.all():
        NewProfile.objects.create(
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


class Migration(migrations.Migration):
    """Migration pour copier les données de l'ancien modèle Profile vers le nouveau modèle Profile."""
    # Cette migration dépend des migrations initiales des deux applications
    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("profiles", "0001_initial"),
    ]
    # Les opérations de la migration : exécution de la fonction de copie des données
    # .noop signifie qu'il n'y a pas d'opération de reverse à faire
    operations = [
        migrations.RunPython(copy_profiles_data, migrations.RunPython.noop),
    ]
