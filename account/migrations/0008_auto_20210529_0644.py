# Generated by Django 3.2.3 on 2021-05-29 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20210528_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academic',
            old_name='phd_percentage',
            new_name='other_percentage',
        ),
        migrations.RenameField(
            model_name='academic',
            old_name='phd_subjects',
            new_name='other_subjects',
        ),
        migrations.RenameField(
            model_name='academic',
            old_name='phd_university',
            new_name='other_university',
        ),
        migrations.RenameField(
            model_name='academic',
            old_name='phd_year',
            new_name='other_year',
        ),
    ]