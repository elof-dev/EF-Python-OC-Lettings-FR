from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    for old_profile in OldProfile.objects.all():
        # user_id exists in both, we reuse the same user FK
        NewProfile.objects.create(
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


def reverse_copy_profiles_data(apps, schema_editor):
    NewProfile = apps.get_model("profiles", "Profile")
    NewProfile.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, reverse_copy_profiles_data),
    ]
