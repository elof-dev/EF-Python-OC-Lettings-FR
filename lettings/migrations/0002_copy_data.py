from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    # Old models (from original app)
    OldAddress = apps.get_model("oc_lettings_site", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")

    # New models (in new app)
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    # 1) copy addresses
    # keep an id mapping old_id -> new_id
    address_id_map = {}

    for old_addr in OldAddress.objects.all():
        new_addr = NewAddress.objects.create(
            number=old_addr.number,
            street=old_addr.street,
            city=old_addr.city,
            state=old_addr.state,
            zip_code=old_addr.zip_code,
            country_iso_code=old_addr.country_iso_code,
        )
        address_id_map[old_addr.id] = new_addr.id

    # 2) copy lettings and re-link to new addresses
    for old_letting in OldLetting.objects.all():
        new_address_id = address_id_map[old_letting.address_id]
        NewLetting.objects.create(
            title=old_letting.title,
            address_id=new_address_id,
        )


def reverse_copy_lettings_data(apps, schema_editor):
    # If we ever rollback, we just delete copied rows in new tables
    NewLetting = apps.get_model("lettings", "Letting")
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting.objects.all().delete()
    NewAddress.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, reverse_copy_lettings_data),
    ]
