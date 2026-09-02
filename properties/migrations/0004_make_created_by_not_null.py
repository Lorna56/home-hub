from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0003_backfill_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="created_by",
            field=models.ForeignKey(
                to="accounts.User",
                on_delete=models.PROTECT,
                related_name="created_properties",
            ),
        ),
    ]
