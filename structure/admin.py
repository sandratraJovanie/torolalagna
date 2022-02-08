from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(etablissements)
admin.site.register(mentions)
admin.site.register(parcours)
admin.site.register(niveaux)



admin.site.site_header = 'Torolalagna Administration'

admin.site.site_title = 'Torolalagna'