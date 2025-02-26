# Generated by Django 5.1.3 on 2024-12-24 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mydb", "0003_alter_have_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="where",
            name="parking_spot",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="where_parking_spot",
                to="mydb.parkingspot",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="where",
            name="parking_lot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="where_parking_lot",
                to="mydb.parkingspot",
            ),
        ),
    ]
