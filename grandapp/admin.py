from django.contrib import admin

from .models import Cell

@admin.register(Cell)
class PetAdmin(admin.ModelAdmin):
    list_display = ['cellLine', 'cellLink', 'tool', 'netzoo', 'network']
