# Generated by Django 3.2.3 on 2021-05-28 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_board', models.CharField(max_length=200, null=True)),
                ('x_year', models.CharField(max_length=20, null=True)),
                ('x_subjects', models.CharField(max_length=300, null=True)),
                ('x_percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('xii_board', models.CharField(max_length=200, null=True)),
                ('xii_year', models.CharField(max_length=20, null=True)),
                ('xii_subjects', models.CharField(max_length=300, null=True)),
                ('xii_percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('degree_board', models.CharField(max_length=200, null=True)),
                ('degree_year', models.CharField(max_length=20, null=True)),
                ('degree_subjects', models.CharField(max_length=300, null=True)),
                ('degree_percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('pg_university', models.CharField(max_length=200, null=True)),
                ('pg_year', models.CharField(max_length=20, null=True)),
                ('pg_subjects', models.CharField(max_length=300, null=True)),
                ('pg_percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('phd_university', models.CharField(max_length=200, null=True)),
                ('phd_year', models.CharField(max_length=20, null=True)),
                ('phd_subjects', models.CharField(max_length=300, null=True)),
                ('phd_percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'Academic',
                'verbose_name_plural': 'Academics',
                'db_table': 'academics',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('father_name', models.CharField(max_length=100, null=True)),
                ('father_occupation', models.CharField(max_length=300, null=True)),
                ('mailing_address', models.EmailField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=20, null=True)),
                ('course', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('academic_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.academic')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'db_table': 'students',
                'managed': True,
            },
        ),
    ]
