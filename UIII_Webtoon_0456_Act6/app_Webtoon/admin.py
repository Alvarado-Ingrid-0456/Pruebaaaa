from django.contrib import admin
from .models import Usuario, Webtoon, Membresia, Suscripcion, Episodio, PaginaEpisodio

admin.site.register(Usuario)
admin.site.register(Webtoon)
admin.site.register(Membresia)
admin.register(Suscripcion)
admin.register(Episodio)
admin.site.register(PaginaEpisodio)