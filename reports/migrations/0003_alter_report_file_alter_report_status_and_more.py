# Generated by Django 4.1.5 on 2023-01-31 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_status_alter_report_title_delete_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='reports/'),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=55),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(default='2023-01-31 11:06:37.735976_report.xlsx', max_length=255),
        ),
    ]
