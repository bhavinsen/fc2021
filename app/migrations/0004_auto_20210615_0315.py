# Generated by Django 2.2.10 on 2021-06-15 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bale',
            old_name='Staple',
            new_name='variety',
        ),
        migrations.AddField(
            model_name='bale',
            name='weightinkg',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]