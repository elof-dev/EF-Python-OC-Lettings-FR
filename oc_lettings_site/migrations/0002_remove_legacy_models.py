from django.db import migrations


class Migration(migrations.Migration):
    """Migration pour supprimer les anciens modèles Address, Letting et Profile."""
    # Cette migration dépend des migrations de copie des données
    # donc ça veut dire que l'exécution de cette migration se fera après celles-ci.
    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0002_copy_data"),
        ("profiles", "0002_copy_data"),
    ]

    operations = [
        # Letting dépend de Address -> on supprime d'abord Letting
        migrations.DeleteModel(name="Letting"),
        migrations.DeleteModel(name="Profile"),
        migrations.DeleteModel(name="Address"),
    ]
