from django.db import migrations


class Migration(migrations.Migration):
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
