# Generated by Django 3.1.7 on 2021-03-08 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0006_recipe_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
    ]
