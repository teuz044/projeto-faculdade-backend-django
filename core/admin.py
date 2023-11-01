from django.contrib import admin

from .models import Pessoa, Acidente

admin.site.register(Pessoa)
admin.site.register(Acidente)