# Generated by Django 4.1.5 on 2023-02-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(default='title_default', max_length=255),
        ),
    ]