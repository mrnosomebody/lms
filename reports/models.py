from django.db import models


class Report(models.Model):
    STATUSES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    title = models.CharField(max_length=255, default='title_default')
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=55,
        choices=STATUSES,
        default='pending'
    )
