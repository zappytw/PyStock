from modulos.inventario import cargar_productos, obtener_producto
from modulos.movimientos import registrar_movimiento
from core.almacenamiento import guardar_datos, cargar_datos, actualizar_datos
from datetime import datetime

def verificar_disponibilidad(id_producto, cantidad):
    producto = obtener_producto(id_producto)

    if producto != []:
        cantidadDisponible = producto["cantidad"]
        if cantidadDisponible >= cantidad:
            haySuficiente = True
        else:
            haySuficiente = False

        return haySuficiente, cantidadDisponible
    else:
        print("ERROR: El producto solicitado no existe o no esta activo en el momento")
        return None, None

def agregar_al_carrito(carrito, id_producto, cantidad_a_agregar):


    haySuficiente, cantidadDisponible = verificar_disponibilidad(id_producto, cantidad_a_agregar) 
    if haySuficiente != None:

        producto_encontrado = False
        for p in carrito:
                if p["id_producto"] == id_producto:
                    producto_a_agregar = p
                    producto_encontrado = True
                    break
                    
        if haySuficiente and not producto_encontrado:
            carrito.append({"id_producto": id_producto,"nombre_producto": obtener_producto(id_producto)["nombre"] , "cantidad": cantidad_a_agregar, "precio": obtener_producto(id_producto)["precio"]})

        elif haySuficiente and producto_encontrado:

            cantidad_total_a_agregar = carrito[carrito.index(producto_a_agregar)]["cantidad"] + cantidad_a_agregar
            if cantidad_total_a_agregar > cantidadDisponible:
                print("ERROR: No hay suficiente cantidad de este producto para añadirlo al carrito")
            else:
                carrito[carrito.index(producto_a_agregar)]["cantidad"] = cantidad_total_a_agregar
        
        else:
            print("ERROR: No hay suficiente cantidad de este producto para añadirlo al carrito")

def quitar_del_carrito(carrito, id_producto = ""):
    producto_encontrado = False

    for p in carrito:
        if p["id_producto"] == id_producto:
            producto_a_quitar = p
            producto_encontrado = True
            break

    if producto_encontrado:
        carrito.pop(carrito.index(producto_a_quitar))
    else:
        print("ERROR: El producto que se quiere quitar no esta en el carrito")

    
def calcular_total(carrito):
    total = 0
    for p in carrito:
        total += p["precio"] * p["cantidad"]

    return total


def registrar_venta(carrito, id_usuario, metodo_pago):
    if len(carrito) == 0:
        print("ERROR: El carrito esta vacio")
        return False

    for p in carrito:
        haySuficiente, disponible = verificar_disponibilidad(p["id_producto"], p["cantidad"])
        if not haySuficiente:
            print(f"ERROR: {p['nombre_producto']} no tiene suficientes existencias. Venta no registrada")
            return False

    datos_ventas = cargar_datos("inventario", "ventas")
    id_mayor = 0
    for v in datos_ventas:
        if v["id_venta"] > id_mayor:
            id_mayor = v["id_venta"]
    id_venta = id_mayor + 1

    for p in carrito:
        registrar_movimiento(p["id_producto"], "salida", p["cantidad"], f"Venta #{id_venta}", id_usuario)

    datos_venta = {"id_venta": id_venta, "carrito": carrito, "id_usuario": id_usuario,
                "fecha_venta": str(datetime.now()), "total_venta": calcular_total(carrito),"metodo_pago": metodo_pago,
                "estado": "completada"}
    guardar_datos(datos_venta, "inventario", "ventas")
    print(f"Venta #{id_venta} registrada. Total: ${calcular_total(carrito):,.0f}")
    return True

def nuevo_metodo_de_pago(nombre_metodo_pago):
    lista_metodos = cargar_datos("inventario", "metodosDePago")
    if nombre_metodo_pago.lower() not in lista_metodos:
        guardar_datos(nombre_metodo_pago.lower(), "inventario", "categorias")
    
    else:
        print("Error: No se permiten duplicados, la categoria ya existe")