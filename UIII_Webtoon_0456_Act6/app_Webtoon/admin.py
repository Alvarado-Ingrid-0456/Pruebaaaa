from django.contrib import admin
from .models import Usuario, Webtoon, Membresia, Suscripcion

admin.site.register(Usuario)
admin.site.register(Webtoon)
admin.site.register(Membresia)
admin.register(Suscripcion)
