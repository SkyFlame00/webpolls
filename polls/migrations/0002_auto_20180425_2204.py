# Generated by Django 2.0.3 on 2018-04-25 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='degree',
            field=models.CharField(blank=True, choices=[('bac', 'Бакалавриат'), ('mag', 'Магистратура')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='educ_end',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='educ_start',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='programme',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='university',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
