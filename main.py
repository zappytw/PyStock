import core, modulos
from core.almacenamiento import cargar_datos, guardar_datos
from modulos.inventario import registrar_producto, nueva_categoria, nueva_unidad, editar_producto
from modulos.movimientos import registrar_movimiento
from modulos.ventas import *
from modulos.usuarios import registrar_usuario, iniciar_sesion, consultar_usuarios
