import core, modulos
from core.almacenamiento import cargar_datos, guardar_datos
from modulos.inventario import registrar_producto, nueva_categoria, nueva_unidad, editar_producto
from modulos.movimientos import registrar_movimiento

from modulos.usuarios import existe_propietario, registrar_propietario, registrar_usuario, iniciar_sesion, cerrar_sesion, consultar_usuarios, editar_usuario, eliminar_usuario
from modulos.abastecimiento import (registrar_proveedor, consultar_proveedores, registrar_pedido, consultar_pedidos, registrar_recepcion, registrar_compra)
from modulos.reportes_comerciales import (reporte_ventas, reporte_compras, reporte_financiero)
from modulos.reportes_inventario import reporte_existencias, reporte_alertas

def menu_inventario(usuarioActual):
    while True:
        print("\n--- INVENTARIO ---")
        print("1. Registrar categoria")
        print("2. Registrar unidad")
        print("3. Registrar producto")
        print("4. Consultar productos")
        print("5. Editar producto")
        print("6. Reporte de existencias")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            nombre = input("Nombre de la categoria: ").strip().lower()
            categorias = cargar_datos("inventario", "categorias")
            if nombre == "":
                print("Error: El nombre es obligatorio")
            elif nombre in categorias:
                print("Error: La categoria ya existe")
            else:
                guardar_datos(nombre, "inventario", "categorias")
                print("Categoria registrada")

        elif opcion == "2":
            nombre = input("Nombre de la unidad: ").strip().lower()
            unidades = cargar_datos("inventario", "unidades")
            if nombre == "":
                print("Error: El nombre es obligatorio")
            elif nombre in unidades:
                print("Error: La unidad ya existe")
            else:
                guardar_datos(nombre, "inventario", "unidades")
                print("Unidad registrada")

        elif opcion == "3":
            nombre = input("Nombre del producto: ")
            categoria = input("Categoria: ").lower()
            unidad = input("Unidad: ").lower()
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad inicial: "))
            minimo = int(input("Existencias minimas: "))
            registrar_producto(nombre, categoria, unidad, precio, cantidad, minimo)

        elif opcion == "4":
            productos = cargar_datos("inventario", "productos")
            for p in productos:
                if p["activo"] == True:
                    print(p)

        elif opcion == "5":
            idProducto = int(input("ID del producto: "))
            dato = input("Dato que desea modificar (nombre, precio, cantidad, etc.): ")
            nuevoValor = input("Nuevo valor: ")
            if dato in ["id", "activo"]:
                print("No se puede modificar ese dato desde este menu")
            else:
                if dato in ["precio", "cantidad", "existencias_minimas"]:
                    nuevoValor = float(nuevoValor)
                    if dato != "precio":
                        nuevoValor = int(nuevoValor)
                editar_producto(idProducto, dato, nuevoValor)

        elif opcion == "6":
            reporte_existencias(usuarioActual)

        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta")


def menu_movimientos(usuarioActual):
    print("\n--- REGISTRAR MOVIMIENTO ---")
    idProducto = int(input("ID del producto: "))
    tipo = input("Tipo (entrada/salida): ").lower()
    cantidad = int(input("Cantidad: "))
    motivo = input("Motivo: ")
    registrar_movimiento(idProducto, tipo, cantidad, motivo, usuarioActual["id"])


def menu_abastecimiento(usuarioActual):
    while True:
        print("\n--- ABASTECIMIENTO ---")
        print("1. Registrar proveedor")
        print("2. Consultar proveedores")
        print("3. Registrar pedido")
        print("4. Consultar pedidos")
        print("5. Registrar recepcion")
        print("6. Registrar compra")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            contacto = input("Contacto: ")
            telefono = input("Telefono: ")
            direccion = input("Direccion: ")
            registrar_proveedor(nombre, contacto, telefono, direccion, usuarioActual)

        elif opcion == "2":
            consultar_proveedores(usuarioActual)

        elif opcion == "3":
            idProveedor = int(input("ID del proveedor: "))
            productos = []
            while True:
                idProducto = int(input("ID del producto (0 para terminar): "))
                if idProducto == 0:
                    break
                cantidad = int(input("Cantidad solicitada: "))
                productos.append({"id_producto": idProducto, "cantidad": cantidad})
            registrar_pedido(idProveedor, productos, usuarioActual)

        elif opcion == "4":
            consultar_pedidos(usuarioActual)

        elif opcion == "5":
            idPedido = int(input("ID del pedido: "))
            productos = []
            while True:
                idProducto = int(input("ID del producto recibido (0 para terminar): "))
                if idProducto == 0:
                    break
                cantidad = int(input("Cantidad recibida: "))
                productos.append({"id_producto": idProducto, "cantidad": cantidad})
            registrar_recepcion(idPedido, productos, usuarioActual)

        elif opcion == "6":
            idPedido = int(input("ID del pedido recibido: "))
            precios = []
            while True:
                idProducto = int(input("ID del producto (0 para terminar): "))
                if idProducto == 0:
                    break
                precio = float(input("Precio de compra por unidad: "))
                precios.append({"id_producto": idProducto, "precio": precio})
            pago = float(input("Valor pagado: "))
            formaPago = input("Forma de pago: ")
            registrar_compra(idPedido, precios, pago, formaPago, usuarioActual)

        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta")


def menu_reportes(usuarioActual):
    while True:
        print("\n--- REPORTES ---")
        print("1. Existencias")
        print("2. Alertas de inventario")
        print("3. Compras")
        print("4. Ventas por periodo")
        print("5. Reporte financiero")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            reporte_existencias(usuarioActual)
        elif opcion == "2":
            reporte_alertas(usuarioActual)
        elif opcion == "3":
            reporte_compras(usuarioActual)
        elif opcion == "4":
            fechaInicio = input("Fecha inicial (AAAA-MM-DD): ")
            fechaFin = input("Fecha final (AAAA-MM-DD): ")
            reporte_ventas(fechaInicio, fechaFin, usuarioActual)
        elif opcion == "5":
            fechaInicio = input("Fecha inicial (AAAA-MM-DD): ")
            fechaFin = input("Fecha final (AAAA-MM-DD): ")
            reporte_financiero(fechaInicio, fechaFin, usuarioActual)
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta")


def menu_usuarios(usuarioActual):
    if usuarioActual["rol"] != "propietario":
        print("Esta opcion es solo para el propietario")
        return

    while True:
        print("\n--- USUARIOS ---")
        print("1. Registrar empleado")
        print("2. Consultar usuarios")
        print("3. Editar empleado")
        print("4. Desactivar empleado")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            nombreUsuario = input("Nombre de usuario: ")
            contrasena = input("Contrasena: ")
            registrar_usuario(nombre, nombreUsuario, contrasena, usuarioActual)
        elif opcion == "2":
            consultar_usuarios(usuarioActual)
        elif opcion == "3":
            idUsuario = int(input("ID del empleado: "))
            nombre = input("Nuevo nombre: ")
            nombreUsuario = input("Nuevo nombre de usuario: ")
            contrasena = input("Nueva contrasena (vacio para conservar): ")
            editar_usuario(idUsuario, nombre, nombreUsuario, contrasena, usuarioActual)
        elif opcion == "4":
            idUsuario = int(input("ID del empleado: "))
            eliminar_usuario(idUsuario, usuarioActual)
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta")


def iniciar_programa():
    if existe_propietario() == False:
        print("--- REGISTRO DEL PROPIETARIO ---")
        nombre = input("Nombre: ")
        nombreUsuario = input("Nombre de usuario: ")
        contrasena = input("Contrasena: ")
        registrar_propietario(nombre, nombreUsuario, contrasena)

    usuarioActual = None
    while usuarioActual == None:
        print("\n--- INICIO DE SESION ---")
        nombreUsuario = input("Usuario: ")
        contrasena = input("Contrasena: ")
        usuarioActual = iniciar_sesion(nombreUsuario, contrasena)

    while usuarioActual != None:
        print("\n--- PYSTOCK ---")
        print("Sesion:", usuarioActual["nombre"], "-", usuarioActual["rol"])
        print("1. Inventario")
        print("2. Registrar movimiento")
        print("3. Abastecimiento")
        print("4. Reportes")
        print("5. Usuarios")
        print("0. Cerrar sesion")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_inventario(usuarioActual)
        elif opcion == "2":
            menu_movimientos(usuarioActual)
        elif opcion == "3":
            menu_abastecimiento(usuarioActual)
        elif opcion == "4":
            menu_reportes(usuarioActual)
        elif opcion == "5":
            menu_usuarios(usuarioActual)
        elif opcion == "0":
            print("Sesion cerrada")
            usuarioActual = None
        else:
            print("Opcion incorrecta")


if __name__ == "__main__":
    iniciar_programa()
