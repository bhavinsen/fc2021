# Generated by Django 2.2.10 on 2021-06-21 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210621_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='testbale',
            name='Bale_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Bale'),
        ),
    ]
