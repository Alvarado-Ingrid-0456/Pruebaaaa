from django.db import models

# ==========================================
# MODELO: USUARIO (ya existente)
# ==========================================
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    biografia = models.TextField(blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[
            ('Lector', 'Lector'),
            ('Autor', 'Autor'),
            ('Admin', 'Admin')
        ],
        default='Lector'
    )

    def __str__(self):
        return self.nombre_usuario

# ==========================================
# MODELO: WEBTOON
# ==========================================
class Webtoon(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    genero = models.CharField(max_length=50)
    fecha_publicacion = models.DateField()
    portada = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('En curso', 'En curso'),
        ('Finalizado', 'Finalizado'),
        ('Hiato', 'Hiato')
    ], default='En curso')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='webtoons')

    def __str__(self):
        return self.titulo
# ==========================================
# MODELO: MEMBRESIA
# ==========================================
class Membresia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    duracion_dias = models.IntegerField()
    beneficios = models.TextField()
    nivel = models.CharField(max_length=20, choices=[
        ('Basico', 'Basico'),
        ('Premium', 'Premium'),
        ('VIP', 'VIP')
    ], default='Basico')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.nombre_usuario}"
# ==========================================
# MODELO: SUBSCRIPCION
# ==========================================
class Suscripcion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='suscripciones')
    webtoon = models.ForeignKey('Webtoon', on_delete=models.CASCADE, related_name='suscriptores')
    fecha_suscripcion = models.DateField()
    notificaciones_activas = models.BooleanField(default=True)
    es_favorito = models.BooleanField(default=False)
    progreso_lectura = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.nombre_usuario} suscrito a {self.webtoon.titulo}"
# ==========================================
# MODELO: EPISODIO
# ==========================================
class Episodio(models.Model):
    webtoon = models.ForeignKey('Webtoon', on_delete=models.CASCADE, related_name='episodios')
    numero_episodio = models.IntegerField()
    titulo_episodio = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    vistas = models.IntegerField(default=0)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    es_gratuito = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.webtoon.titulo} - Episodio {self.numero_episodio}: {self.titulo_episodio}"
# ==========================================
# MODELO: PAGINA EPISODIO
# ==========================================
class PaginaEpisodio(models.Model):
    episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE, related_name='paginas')
    numero_pagina = models.IntegerField()
    imagen_url = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    fecha_subida = models.DateTimeField()
    ancho_pixel = models.IntegerField()
    alto_pixel = models.IntegerField()

    def __str__(self):
        return f"Página {self.numero_pagina} del {self.episodio.titulo_episodio}"

