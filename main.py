import core, modulos
from core.almacenamiento import cargar_datos, guardar_datos
from modulos.inventario import registrar_producto, nueva_categoria, nueva_unidad, editar_producto
from modulos.movimientos import registrar_movimiento

from modulos.usuarios import existe_propietario, registrar_propietario, registrar_usuario, iniciar_sesion, cerrar_sesion, consultar_usuarios, editar_usuario, eliminar_usuario
from modulos.abastecimiento import (registrar_proveedor, consultar_proveedores, registrar_pedido, consultar_pedidos, registrar_recepcion, registrar_compra)
from modulos.reportes_comerciales import (reporte_ventas, reporte_compras, reporte_financiero)
from modulos.reportes_inventario import reporte_existencias, reporte_alertas