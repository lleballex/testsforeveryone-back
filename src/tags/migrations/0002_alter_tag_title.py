# Generated by Django 4.0.3 on 2022-04-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
