# Generated by Django 4.2.13 on 2024-06-12 03:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_remove_receta_categoria_remove_receta_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoria',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
