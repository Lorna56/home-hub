from django.db import migrations


def set_created_by(apps, schema_editor):
    Property = apps.get_model("properties", "Property")
    # Use update to avoid save() side-effects
    for p in Property.objects.all():
        owner = getattr(p, "owner", None)
        if owner:
            Property.objects.filter(pk=p.pk).update(created_by=owner)


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_add_created_by"),
    ]

    operations = [
        migrations.RunPython(set_created_by, reverse_code=migrations.RunPython.noop),
    ]
