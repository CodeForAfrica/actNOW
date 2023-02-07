from django.db import migrations


def link_profiles(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    OrganisationProfile = apps.get_model("profiles", "OrganisationProfile")
    UserProfile = apps.get_model("profiles", "UserProfile")

    for organisation in OrganisationProfile.objects.all():
        profile = Profile(organisation_profile=organisation)
        profile.save()

    for user in UserProfile.objects.all():
        profile = Profile(user_profile=user)
        profile.save()


def unlink_profiles(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0010_profile"),
    ]

    operations = [
        migrations.RunPython(link_profiles, unlink_profiles),
    ]
