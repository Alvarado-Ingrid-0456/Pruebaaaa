# app_Webtoon/urls.py
from django.urls import path
from . import views

app_name = 'app_Webtoon'

urlpatterns = [
    path('', views.inicio_webtoon, name='inicio'),
    # USUARIO
    path('usuario/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuario/ver/', views.ver_usuario, name='ver_usuario'),
    path('usuario/actualizar/<int:usuario_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuario/realizar_actualizacion/<int:usuario_id>/', views.realizar_actualizacion_usuario, name='realizar_actualizacion_usuario'),
    path('usuario/borrar/<int:usuario_id>/', views.borrar_usuario, name='borrar_usuario'),
    # WEBTOON
    path('webtoons/agregar/', views.agregar_webtoon, name='agregar_webtoon'),
    path('webtoons/ver/', views.ver_webtoons, name='ver_webtoons'),
    path('webtoons/actualizar/<int:webtoon_id>/', views.actualizar_webtoon, name='actualizar_webtoon'),
    path('webtoons/realizar_actualizacion/<int:webtoon_id>/', views.realizar_actualizacion_webtoon, name='realizar_actualizacion_webtoon'),
    path('webtoons/borrar/<int:webtoon_id>/', views.borrar_webtoon, name='borrar_webtoon'),
    # MEMBRESIA
    path('agregar_membresia/', views.agregar_membresia, name='agregar_membresia'),
    path('ver_membresia/', views.ver_membresia, name='ver_membresia'),
    path('actualizar_membresia/<int:membresia_id>/', views.actualizar_membresia, name='actualizar_membresia'),
    path('realizar_actualizacion_membresia/<int:membresia_id>/', views.realizar_actualizacion_membresia, name='realizar_actualizacion_membresia'),
    path('borrar_membresia/<int:membresia_id>/', views.borrar_membresia, name='borrar_membresia'),
    # SUSCRIPCIONES
    path('subscripcion/agregar/', views.agregar_subscripcion, name='agregar_subscripcion'),
    path('subscripcion/ver/', views.ver_subscripcion, name='ver_subscripcion'),
    path('subscripcion/actualizar/<int:subscripcion_id>/', views.actualizar_subscripcion, name='actualizar_subscripcion'),
    path('subscripcion/realizar_actualizacion/<int:subscripcion_id>/', views.realizar_actualizacion_subscripcion, name='realizar_actualizacion_subscripcion'),
    path('subscripcion/borrar/<int:subscripcion_id>/', views.borrar_subscripcion, name='borrar_subscripcion'),
]
