from django.db import models


class Messages(models.Model):
    user_id = models.IntegerField()
    text = models.TextField(blank=True)
    status = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
