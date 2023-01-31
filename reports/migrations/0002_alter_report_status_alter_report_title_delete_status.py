# Generated by Django 4.1.5 on 2023-01-31 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=55),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(default='2023-01-31 11:05:13.948240_report.xlsx', max_length=255),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]