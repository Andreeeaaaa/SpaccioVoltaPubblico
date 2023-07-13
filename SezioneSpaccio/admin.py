from django.contrib import admin
from . import models

# Register your models here so that they show up in the
# admin page

admin.site.register(models.Sezione)
admin.site.register(models.Libro)

