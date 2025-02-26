# Generated by Django 5.1.3 on 2024-12-25 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mydb", "0005_alter_where_parking_spot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="exit_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="record",
            name="fee",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
    ]
