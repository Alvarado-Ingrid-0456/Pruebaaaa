# app_Webtoon/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Usuario, Webtoon, Membresia, Suscripcion, Episodio, PaginaEpisodio
# ==========================================
# PÁGINA DE INICIO
# ==========================================
def inicio_webtoon(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    webtoons = Webtoon.objects.all().order_by('-fecha_publicacion')
    return render(request, 'inicio.html', {'usuarios': usuarios, 'webtoons': webtoons})


# ==========================================
# CRUD USUARIOS (ya funcionando)
# ==========================================
def agregar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario', '')
        email = request.POST.get('email', '')
        contraseña = request.POST.get('contraseña', '')
        avatar = request.POST.get('avatar', '')
        biografia = request.POST.get('biografia', '')
        tipo = request.POST.get('tipo_usuario', 'Lector')

        usuario = Usuario(
            nombre_usuario=nombre,
            email=email,
            contraseña=make_password(contraseña),
            avatar=avatar,
            biografia=biografia,
            tipo_usuario=tipo
        )
        usuario.save()
        return redirect('app_Webtoon:ver_usuario')
    return render(request, 'usuario/agregar_usuario.html')


def ver_usuario(request):
    usuarios = Usuario.objects.all().order_by('id')
    return render(request, 'usuario/ver_usuario.html', {'usuarios': usuarios})


def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})


def realizar_actualizacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.nombre_usuario = request.POST.get('nombre_usuario', usuario.nombre_usuario)
        usuario.email = request.POST.get('email', usuario.email)
        nueva_contraseña = request.POST.get('contraseña', '')
        if nueva_contraseña:
            usuario.contraseña = make_password(nueva_contraseña)
        usuario.avatar = request.POST.get('avatar', usuario.avatar)
        usuario.biografia = request.POST.get('biografia', usuario.biografia)
        usuario.tipo_usuario = request.POST.get('tipo_usuario', usuario.tipo_usuario)
        usuario.save()
        return redirect('app_Webtoon:ver_usuario')
    return redirect('app_Webtoon:actualizar_usuario', usuario_id=usuario.id)


def borrar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('app_Webtoon:ver_usuario')
    return render(request, 'usuario/borrar_usuario.html', {'usuario': usuario})


# ==========================================
# CRUD WEBTOONS
# ==========================================

# --- AGREGAR ---
def agregar_webtoon(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '')
        descripcion = request.POST.get('descripcion', '')
        genero = request.POST.get('genero', '')
        fecha_publicacion = request.POST.get('fecha_publicacion', '')
        portada = request.POST.get('portada', '')
        estado = request.POST.get('estado', 'En curso')
        autor_id = request.POST.get('autor', None)

        autor = None
        if autor_id:
            try:
                autor = Usuario.objects.get(id=int(autor_id))
            except Usuario.DoesNotExist:
                autor = None

        webtoon = Webtoon(
            titulo=titulo,
            descripcion=descripcion,
            genero=genero,
            fecha_publicacion=fecha_publicacion or timezone.now().date(),
            portada=portada,
            estado=estado,
            autor=autor
        )
        webtoon.save()
        return redirect('app_Webtoon:ver_webtoons')

    autores = Usuario.objects.all()
    return render(request, 'webtoons/agregar_webtoon.html', {'autores': autores})


# --- VER ---
def ver_webtoons(request):
    webtoons = Webtoon.objects.all().order_by('id')
    return render(request, 'webtoons/ver_webtoons.html', {'webtoons': webtoons})


# --- ACTUALIZAR (mostrar formulario) ---
def actualizar_webtoon(request, webtoon_id):
    webtoon = get_object_or_404(Webtoon, id=webtoon_id)
    autores = Usuario.objects.all()
    return render(request, 'webtoons/actualizar_webtoon.html', {'webtoon': webtoon, 'autores': autores})


# --- REALIZAR ACTUALIZACIÓN ---
def realizar_actualizacion_webtoon(request, webtoon_id):
    webtoon = get_object_or_404(Webtoon, id=webtoon_id)
    if request.method == 'POST':
        webtoon.titulo = request.POST.get('titulo', webtoon.titulo)
        webtoon.descripcion = request.POST.get('descripcion', webtoon.descripcion)
        webtoon.genero = request.POST.get('genero', webtoon.genero)
        fecha_pub = request.POST.get('fecha_publicacion', None)
        if fecha_pub:
            webtoon.fecha_publicacion = fecha_pub
        webtoon.portada = request.POST.get('portada', webtoon.portada)
        webtoon.estado = request.POST.get('estado', webtoon.estado)

        autor_id = request.POST.get('autor', None)
        if autor_id:
            try:
                webtoon.autor = Usuario.objects.get(id=int(autor_id))
            except Usuario.DoesNotExist:
                pass

        webtoon.save()
        return redirect('app_Webtoon:ver_webtoons')
    return redirect('app_Webtoon:actualizar_webtoon', webtoon_id=webtoon.id)


# --- BORRAR ---
def borrar_webtoon(request, webtoon_id):
    webtoon = get_object_or_404(Webtoon, id=webtoon_id)
    if request.method == 'POST':
        webtoon.delete()
        return redirect('app_Webtoon:ver_webtoons')
    return render(request, 'webtoons/borrar_webtoon.html', {'webtoon': webtoon})

# ==========================================
# CRUD MEMBRESÍAS
# ==========================================

# --- AGREGAR ---
def agregar_membresia(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST.get('precio', 0)
        duracion_dias = request.POST.get('duracion_dias', 0)
        beneficios = request.POST.get('beneficios', '')
        nivel = request.POST.get('nivel', 'Basico')
        usuario_id = request.POST.get('usuario', None)
        webtoon_id = request.POST.get('webtoon', None)

        usuario = None
        webtoon = None

        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=int(usuario_id))
            except Usuario.DoesNotExist:
                usuario = None

        if webtoon_id:
            try:
                webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                webtoon = None

        Membresia.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            duracion_dias=duracion_dias,
            beneficios=beneficios,
            nivel=nivel,
            usuario=usuario,
            webtoon=webtoon
        )
        return redirect('app_Webtoon:ver_membresia')

    usuarios = Usuario.objects.all()
    webtoons = Webtoon.objects.all()
    return render(request, 'membresia/agregar_membresia.html', {
        'usuarios': usuarios,
        'webtoons': webtoons
    })


# --- VER ---
def ver_membresia(request):
    membresias = Membresia.objects.all().order_by('id')
    return render(request, 'membresia/ver_membresia.html', {'membresias': membresias})


# --- ACTUALIZAR (mostrar formulario) ---
def actualizar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    usuarios = Usuario.objects.all()
    webtoons = Webtoon.objects.all()
    return render(request, 'membresia/actualizar_membresia.html', {
        'membresia': membresia,
        'usuarios': usuarios,
        'webtoons': webtoons
    })


# --- REALIZAR ACTUALIZACIÓN ---
def realizar_actualizacion_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    if request.method == 'POST':
        membresia.nombre = request.POST.get('nombre', membresia.nombre)
        membresia.descripcion = request.POST.get('descripcion', membresia.descripcion)
        membresia.precio = request.POST.get('precio', membresia.precio)
        membresia.duracion_dias = request.POST.get('duracion_dias', membresia.duracion_dias)
        membresia.beneficios = request.POST.get('beneficios', membresia.beneficios)
        membresia.nivel = request.POST.get('nivel', membresia.nivel)

        usuario_id = request.POST.get('usuario', None)
        webtoon_id = request.POST.get('webtoon', None)

        if usuario_id:
            try:
                membresia.usuario = Usuario.objects.get(id=int(usuario_id))
            except Usuario.DoesNotExist:
                pass

        if webtoon_id:
            try:
                membresia.webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                pass

        membresia.save()
        return redirect('app_Webtoon:ver_membresia')

    return redirect('app_Webtoon:actualizar_membresia', membresia_id=membresia.id)


# --- BORRAR ---
def borrar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    if request.method == 'POST':
        membresia.delete()
        return redirect('app_Webtoon:ver_membresia')
    return render(request, 'membresia/borrar_membresia.html', {'membresia': membresia})

# ==========================================
# CRUD SUSCRIPCIONES
# ==========================================
def agregar_subscripcion(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario', None)
        webtoon_id = request.POST.get('webtoon', None)
        fecha = request.POST.get('fecha_suscripcion', '')  # formato YYYY-MM-DD
        notificaciones = True if request.POST.get('notificaciones_activas') == 'on' else False
        es_favorito = True if request.POST.get('es_favorito') == 'on' else False
        progreso = request.POST.get('progreso_lectura', None)

        usuario = None
        webtoon = None
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=int(usuario_id))
            except Usuario.DoesNotExist:
                usuario = None
        if webtoon_id:
            try:
                webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                webtoon = None

        # Si no se proporciona fecha, usar fecha actual
        fecha_obj = fecha or timezone.now().date()

        if usuario and webtoon:
            Suscripcion.objects.create(
                usuario=usuario,
                webtoon=webtoon,
                fecha_suscripcion=fecha_obj,
                notificaciones_activas=notificaciones,
                es_favorito=es_favorito,
                progreso_lectura=progreso or None
            )

        return redirect('app_Webtoon:ver_subscripcion')

    usuarios = Usuario.objects.all()
    webtoons = Webtoon.objects.all()
    return render(request, 'subscripcion/agregar_subscripcion.html', {
        'usuarios': usuarios,
        'webtoons': webtoons
    })


def ver_subscripcion(request):
    subs = Suscripcion.objects.all().order_by('-fecha_suscripcion')
    return render(request, 'subscripcion/ver_subscripcion.html', {'subscripciones': subs})


def actualizar_subscripcion(request, subscripcion_id):
    subs = get_object_or_404(Suscripcion, id=subscripcion_id)
    usuarios = Usuario.objects.all()
    webtoons = Webtoon.objects.all()
    return render(request, 'subscripcion/actualizar_subscripcion.html', {
        'subs': subs, 'usuarios': usuarios, 'webtoons': webtoons
    })


def realizar_actualizacion_subscripcion(request, subscripcion_id):
    subs = get_object_or_404(Suscripcion, id=subscripcion_id)
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario', None)
        webtoon_id = request.POST.get('webtoon', None)
        fecha = request.POST.get('fecha_suscripcion', None)
        subs.notificaciones_activas = True if request.POST.get('notificaciones_activas') == 'on' else False
        subs.es_favorito = True if request.POST.get('es_favorito') == 'on' else False
        progreso = request.POST.get('progreso_lectura', None)

        if usuario_id:
            try:
                subs.usuario = Usuario.objects.get(id=int(usuario_id))
            except Usuario.DoesNotExist:
                pass
        if webtoon_id:
            try:
                subs.webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                pass
        if fecha:
            subs.fecha_suscripcion = fecha
        subs.progreso_lectura = progreso or subs.progreso_lectura

        subs.save()
        return redirect('app_Webtoon:ver_subscripcion')

    return redirect('app_Webtoon:actualizar_subscripcion', subscripcion_id=subs.id)


def borrar_subscripcion(request, subscripcion_id):
    subs = get_object_or_404(Suscripcion, id=subscripcion_id)
    if request.method == 'POST':
        subs.delete()
        return redirect('app_Webtoon:ver_subscripcion')
    return render(request, 'subscripcion/borrar_subscripcion.html', {'subs': subs})

# ==========================================
# CRUD EPISODIOS
# ==========================================

def agregar_episodio(request):
    if request.method == 'POST':
        webtoon_id = request.POST.get('webtoon')
        numero = request.POST.get('numero_episodio')
        titulo = request.POST.get('titulo_episodio')
        fecha = request.POST.get('fecha_publicacion')
        vistas = request.POST.get('vistas', 0)
        calificacion = request.POST.get('calificacion_promedio', 0.00)
        es_gratuito = True if request.POST.get('es_gratuito') == 'on' else False

        webtoon = None
        if webtoon_id:
            try:
                webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                webtoon = None

        fecha_obj = fecha or timezone.now().date()

        if webtoon:
            Episodio.objects.create(
                webtoon=webtoon,
                numero_episodio=numero,
                titulo_episodio=titulo,
                fecha_publicacion=fecha_obj,
                vistas=vistas,
                calificacion_promedio=calificacion,
                es_gratuito=es_gratuito
            )

        return redirect('app_Webtoon:ver_episodio')

    webtoons = Webtoon.objects.all()
    return render(request, 'episodio/agregar_episodio.html', {'webtoons': webtoons})


def ver_episodio(request):
    episodios = Episodio.objects.all().order_by('-fecha_publicacion')
    return render(request, 'episodio/ver_episodio.html', {'episodios': episodios})


def actualizar_episodio(request, episodio_id):
    episodio = get_object_or_404(Episodio, id=episodio_id)
    webtoons = Webtoon.objects.all()
    return render(request, 'episodio/actualizar_episodio.html', {'episodio': episodio, 'webtoons': webtoons})


def realizar_actualizacion_episodio(request, episodio_id):
    episodio = get_object_or_404(Episodio, id=episodio_id)
    if request.method == 'POST':
        webtoon_id = request.POST.get('webtoon')
        episodio.numero_episodio = request.POST.get('numero_episodio')
        episodio.titulo_episodio = request.POST.get('titulo_episodio')
        episodio.fecha_publicacion = request.POST.get('fecha_publicacion')
        episodio.vistas = request.POST.get('vistas', 0)
        episodio.calificacion_promedio = request.POST.get('calificacion_promedio', 0.00)
        episodio.es_gratuito = True if request.POST.get('es_gratuito') == 'on' else False

        if webtoon_id:
            try:
                episodio.webtoon = Webtoon.objects.get(id=int(webtoon_id))
            except Webtoon.DoesNotExist:
                pass

        episodio.save()
        return redirect('app_Webtoon:ver_episodio')
    return redirect('app_Webtoon:actualizar_episodio', episodio_id=episodio.id)


def borrar_episodio(request, episodio_id):
    episodio = get_object_or_404(Episodio, id=episodio_id)
    if request.method == 'POST':
        episodio.delete()
        return redirect('app_Webtoon:ver_episodio')
    return render(request, 'episodio/borrar_episodio.html', {'episodio': episodio})

# ==========================================
# CRUD PAGINA EPISODIO
# ==========================================

# --- AGREGAR ---
def agregar_pagEpisodio(request):
    if request.method == 'POST':
        episodio_id = request.POST.get('episodio', None)
        numero_pagina = request.POST.get('numero_pagina', '')
        imagen_url = request.POST.get('imagen_url', '')
        alt_text = request.POST.get('alt_text', '')
        fecha_subida = request.POST.get('fecha_subida', timezone.now())
        ancho_pixel = request.POST.get('ancho_pixel', 0)
        alto_pixel = request.POST.get('alto_pixel', 0)

        episodio = None
        if episodio_id:
            try:
                episodio = Episodio.objects.get(id=int(episodio_id))
            except Episodio.DoesNotExist:
                episodio = None

        pag = PaginaEpisodio(
            episodio=episodio,
            numero_pagina=numero_pagina,
            imagen_url=imagen_url,
            alt_text=alt_text,
            fecha_subida=fecha_subida,
            ancho_pixel=ancho_pixel,
            alto_pixel=alto_pixel
        )
        pag.save()
        return redirect('app_Webtoon:ver_pagEpisodio')

    episodios = Episodio.objects.all()
    return render(request, 'pagEpisodio/agregar_pagEpisodio.html', {'episodios': episodios})


# --- VER ---
def ver_pagEpisodio(request):
    paginas = PaginaEpisodio.objects.all().order_by('id')
    return render(request, 'pagEpisodio/ver_pagEpisodio.html', {'paginas': paginas})


# --- ACTUALIZAR (mostrar formulario) ---
def actualizar_pagEpisodio(request, pagina_id):
    pagina = get_object_or_404(PaginaEpisodio, id=pagina_id)
    episodios = Episodio.objects.all()
    return render(request, 'pagEpisodio/actualizar_pagEpisodio.html', {'pagina': pagina, 'episodios': episodios})


# --- REALIZAR ACTUALIZACIÓN ---
def realizar_actualizacion_pagEpisodio(request, pagina_id):
    pagina = get_object_or_404(PaginaEpisodio, id=pagina_id)
    if request.method == 'POST':
        pagina.numero_pagina = request.POST.get('numero_pagina', pagina.numero_pagina)
        pagina.imagen_url = request.POST.get('imagen_url', pagina.imagen_url)
        pagina.alt_text = request.POST.get('alt_text', pagina.alt_text)
        pagina.fecha_subida = request.POST.get('fecha_subida', pagina.fecha_subida)
        pagina.ancho_pixel = request.POST.get('ancho_pixel', pagina.ancho_pixel)
        pagina.alto_pixel = request.POST.get('alto_pixel', pagina.alto_pixel)

        episodio_id = request.POST.get('episodio', None)
        if episodio_id:
            try:
                pagina.episodio = Episodio.objects.get(id=int(episodio_id))
            except Episodio.DoesNotExist:
                pass

        pagina.save()
        return redirect('app_Webtoon:ver_pagEpisodio')
    return redirect('app_Webtoon:actualizar_pagEpisodio', pagina_id=pagina.id)


# --- BORRAR ---
def borrar_pagEpisodio(request, pagina_id):
    pagina = get_object_or_404(PaginaEpisodio, id=pagina_id)
    if request.method == 'POST':
        pagina.delete()
        return redirect('app_Webtoon:ver_pagEpisodio')
    return render(request, 'pagEpisodio/borrar_pagEpisodio.html', {'pagina': pagina})