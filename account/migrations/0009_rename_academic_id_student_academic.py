# Generated by Django 3.2.3 on 2021-05-31 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210529_0644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='academic_id',
            new_name='academic',
        ),
    ]
