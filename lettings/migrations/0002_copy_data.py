from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """FFonction qui copie les données des anciens modèles Address et Letting vers les nouveaux modèles."""
    # Récupération des anciens modèles
    OldAddress = apps.get_model("oc_lettings_site", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")

    # Récupération des nouveaux modèles
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    # 1) dictionnaire qui stocke des correspondances d'IDs entre anciennes et nouvelles adresses
    address_id_map = {}
    # pour chaque ancienne adresse, on crée une nouvelle adresse
    for old_addr in OldAddress.objects.all():
        new_addr = NewAddress.objects.create(
            number=old_addr.number,
            street=old_addr.street,
            city=old_addr.city,
            state=old_addr.state,
            zip_code=old_addr.zip_code,
            country_iso_code=old_addr.country_iso_code,
        )
        # on stocke la correspondance d'ID
        address_id_map[old_addr.id] = new_addr.id

    # 2) copie des lettings et re-liaison aux nouvelles adresses
    for old_letting in OldLetting.objects.all():
        new_address_id = address_id_map[old_letting.address_id]
        NewLetting.objects.create(
            title=old_letting.title,
            address_id=new_address_id,
        )


class Migration(migrations.Migration):
    """Migration pour copier les données des anciens modèles Address et Letting vers les nouveaux modèles."""
    # Cette migration dépend des migrations initiales des deux applications
    # donc ça veut dire que l'exécution de cette migration se fera après celles-ci.
    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0001_initial"),
    ]
    # Les opérations de la migration : exécution de la fonction de copie des données
    # .noop signifie qu'il n'y a pas d'opération de reverse à faire
    operations = [
        migrations.RunPython(copy_lettings_data, migrations.RunPython.noop),
    ]
