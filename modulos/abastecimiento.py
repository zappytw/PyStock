from core.almacenamiento import cargar_datos, guardar_datos, actualizar_datos
from datetime import datetime
from modulos.movimientos import registrar_movimiento


def registrar_proveedor(nombre, contacto, telefono, direccion, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para registrar proveedores")
        return

    proveedores = cargar_datos("abastecimiento", "proveedores")

    if nombre == "" or telefono == "":
        print("Error: El nombre y telefono son obligatorios")
        return

    for p in proveedores:
        if p["nombre"].lower() == nombre.lower():
            print("Error: El proveedor ya existe")
            return

    idMayor = 0
    for p in proveedores:
        if p["id"] > idMayor:
            idMayor = p["id"]

    datosProveedor = {
        "id": idMayor + 1,
        "nombre": nombre,
        "contacto": contacto,
        "telefono": telefono,
        "direccion": direccion
    }

    guardar_datos(datosProveedor, "abastecimiento", "proveedores")
    print("Proveedor registrado con exito!")


def consultar_proveedores(usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para consultar proveedores")
        return

    proveedores = cargar_datos("abastecimiento", "proveedores")

    for p in proveedores:
        print("ID:", p["id"], "| Nombre:", p["nombre"],
              "| Contacto:", p["contacto"], "| Telefono:", p["telefono"],
              "| Direccion:", p["direccion"])


def registrar_pedido(idProveedor, productos, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para registrar pedidos")
        return

    proveedores = cargar_datos("abastecimiento", "proveedores")
    proveedorEncontrado = False

    for p in proveedores:
        if p["id"] == idProveedor:
            proveedorEncontrado = True

    if proveedorEncontrado == False:
        print("Error: No se encontro el proveedor")
        return

    if len(productos) == 0:
        print("Error: El pedido no tiene productos")
        return

    listaProductos = cargar_datos("inventario", "productos")
    for item in productos:
        productoEncontrado = False
        for p in listaProductos:
            if p["id"] == item["id_producto"]:
                productoEncontrado = True
        if productoEncontrado == False or item["cantidad"] <= 0:
            print("Error: Producto o cantidad incorrecta")
            return

    pedidos = cargar_datos("abastecimiento", "pedidos")
    idMayor = 0
    for p in pedidos:
        if p["id"] > idMayor:
            idMayor = p["id"]

    datosPedido = {
        "id": idMayor + 1,
        "id_proveedor": idProveedor,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "estado": "pendiente",
        "productos": productos
    }

    guardar_datos(datosPedido, "abastecimiento", "pedidos")
    print("Pedido registrado con ID:", idMayor + 1)


def consultar_pedidos(usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para consultar pedidos")
        return

    pedidos = cargar_datos("abastecimiento", "pedidos")

    for pedido in pedidos:
        print("Pedido:", pedido["id"], "| Proveedor:", pedido["id_proveedor"],
              "| Fecha:", pedido["fecha"], "| Estado:", pedido["estado"])
        for p in pedido["productos"]:
            print("Producto:", p["id_producto"], "| Cantidad pedida:", p["cantidad"],
                  "| Cantidad recibida:", p["cantidad_recibida"])


def registrar_recepcion(idPedido, productosRecibidos, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para registrar recepciones")
        return

    pedidos = cargar_datos("abastecimiento", "pedidos")
    encontrado = False

    for pedido in pedidos:
        if pedido["id"] == idPedido:
            encontrado = True
            pedidoActual = pedido

    if encontrado == False:
        print("Error: No se encontro el pedido")
        return

    # Comprobar cantidades antes de registrar los movimientos.
    for recibido in productosRecibidos:
        productoPedido = False
        for p in pedidoActual["productos"]:
            if p["id_producto"] == recibido["id_producto"]:
                productoPedido = True
                if recibido["cantidad"] < 0 or p["cantidad_recibida"] + recibido["cantidad"] > p["cantidad"]:
                    print("Error: Cantidad recibida incorrecta")
                    return
        if productoPedido == False:
            print("Error: El producto no pertenece al pedido")
            return

    for recibido in productosRecibidos:
        for p in pedidoActual["productos"]:
            if p["id_producto"] == recibido["id_producto"]:
                if recibido["cantidad"] > 0:
                    registrar_movimiento(recibido["id_producto"], "entrada",
                                         recibido["cantidad"], "Recepcion pedido " + str(idPedido),
                                         usuarioActual["id"])
                p["cantidad_recibida"] += recibido["cantidad"]

    completo = True
    for p in pedidoActual["productos"]:
        if p["cantidad_recibida"] < p["cantidad"]:
            completo = False

    if completo == True:
        pedidoActual["estado"] = "recibido"
    else:
        pedidoActual["estado"] = "parcial"

    actualizar_datos(pedidos, "abastecimiento", "pedidos")
    print("Recepcion registrada!")


def registrar_compra(idPedido, precios, pago, formaPago, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para registrar compras")
        return

    pedidos = cargar_datos("abastecimiento", "pedidos")
    pedidoEncontrado = False

    for p in pedidos:
        if p["id"] == idPedido:
            pedidoEncontrado = True
            pedido = p

    if pedidoEncontrado == False:
        print("Error: No se encontro el pedido")
        return

    total = 0
    productosCompra = []

    for precio in precios:
        cantidad = 0
        for p in pedido["productos"]:
            if p["id_producto"] == precio["id_producto"]:
                cantidad = p["cantidad_recibida"]

        if cantidad == 0 or precio["precio"] <= 0:
            print("Error: Revise el producto, la cantidad recibida y el precio")
            return

        subtotal = cantidad * precio["precio"]
        total = total + subtotal
        productosCompra.append({
            "id_producto": precio["id_producto"],
            "cantidad": cantidad,
            "precio_compra": precio["precio"],
            "subtotal": subtotal
        })

    if pago < 0 or pago > total:
        print("Error: El pago no puede ser negativo ni superar el total")
        return

    compras = cargar_datos("abastecimiento", "compras")
    idMayor = 0
    for c in compras:
        if c["id"] > idMayor:
            idMayor = c["id"]

    datosCompra = {
        "id": idMayor + 1,
        "id_pedido": idPedido,
        "id_proveedor": pedido["id_proveedor"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "productos": productosCompra,
        "total": total,
        "pagado": pago,
        "forma_pago": formaPago
    }

    guardar_datos(datosCompra, "abastecimiento", "compras")
    print("Compra registrada con exito!")
