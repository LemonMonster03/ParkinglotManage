# Generated by Django 5.1.3 on 2024-12-24 09:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mydb", "0002_admin_owner_record_remove_car_color_remove_car_model_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="have",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="manage",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="own",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="where",
            unique_together=set(),
        ),
    ]
