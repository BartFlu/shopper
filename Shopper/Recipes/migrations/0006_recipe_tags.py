# Generated by Django 3.1.7 on 2021-03-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0005_remove_recipe_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='Recipes.Tag'),
        ),
    ]
