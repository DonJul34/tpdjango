# Generated by Django 3.2.25 on 2024-11-27 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='preferred_language',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=10),
        ),
    ]
