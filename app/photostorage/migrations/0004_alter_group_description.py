# Generated by Django 5.2 on 2025-04-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photostorage', '0003_alter_family_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание группы'),
        ),
    ]
