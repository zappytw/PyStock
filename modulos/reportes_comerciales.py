import os
from datetime import datetime
from core.almacenamiento import cargar_datos


def reporte_ventas(fechaInicio, fechaFin, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede consultar las ventas")
        return

    if os.path.exists("data/ventas/ventas.json") == False:
        print("No existe el registro de ventas. Falta implementar el modulo de ventas.")
        return

    ventas = cargar_datos("ventas", "ventas")
    total = 0

    print("\n--- REPORTE DE VENTAS ---")
    for v in ventas:
        fecha = v["fecha"][:10]
        if fecha >= fechaInicio and fecha <= fechaFin:
            print(v)
            total = total + v["total"]

    print("Total de ventas:", total)


def reporte_compras(usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede consultar las compras")
        return

    compras = cargar_datos("abastecimiento", "compras")
    proveedores = cargar_datos("abastecimiento", "proveedores")

    print("\n--- REPORTE DE COMPRAS ---")
    for c in compras:
        nombreProveedor = "No encontrado"
        for p in proveedores:
            if p["id"] == c["id_proveedor"]:
                nombreProveedor = p["nombre"]

        print("Compra:", c["id"], "| Proveedor:", nombreProveedor,
              "| Fecha:", c["fecha"], "| Total:", c["total"])
        for producto in c["productos"]:
            print("Producto:", producto["id_producto"],
                  "| Cantidad:", producto["cantidad"],
                  "| Precio:", producto["precio_compra"])


def reporte_financiero(fechaInicio, fechaFin, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede consultar el reporte financiero")
        return

    if os.path.exists("data/ventas/ventas.json") == False:
        print("No se puede calcular la utilidad porque no existe el registro de ventas")
        return

    ventas = cargar_datos("ventas", "ventas")
    compras = cargar_datos("abastecimiento", "compras")
    ingresos = 0
    costos = 0

    for v in ventas:
        fecha = v["fecha"][:10]
        if fecha >= fechaInicio and fecha <= fechaFin:
            ingresos = ingresos + v["total"]

    for c in compras:
        if c["fecha"] >= fechaInicio and c["fecha"] <= fechaFin:
            costos = costos + c["total"]

    utilidad = ingresos - costos

    print("Ingresos:", ingresos)
    print("Costos de compra:", costos)
    print("Utilidad estimada:", utilidad)
