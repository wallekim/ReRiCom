from django.contrib import admin
from re_api import models


@admin.register(models.Messages)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'text', 'status')
