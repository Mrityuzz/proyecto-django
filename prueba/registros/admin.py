from django.contrib import admin
from registros.models import Alumnos

# Register your models here.

class AdministarModelo(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Alumnos, AdministarModelo)