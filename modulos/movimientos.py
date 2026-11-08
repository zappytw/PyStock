from core.almacenamiento import cargar_datos, guardar_datos, actualizar_datos
from datetime import datetime

def registrar_movimiento(id_producto, tipo, cantidadMovimiento, motivo, id_usuario):
    listaProductos = cargar_datos("inventario", "productos")
    datosMovimiento = {"id_producto": id_producto, "tipo_movimiento": tipo, "cantidad": cantidadMovimiento, "motivo": motivo, "id_usuario": id_usuario, "fecha_movimiento": str(datetime.now())}

    encontrado = False

    match tipo:
        case "entrada":
            for p in listaProductos:
                if p["id"] == id_producto:
                    encontrado = True
                    p["cantidad"] += cantidadMovimiento
                    break
        case "salida":
            for p in listaProductos:
                if p["id"] == id_producto:
                    encontrado = True

                    if p["cantidad"] >= cantidadMovimiento: ##Que la cantidad del movimiento sea negativa o no se validara en main
                        p["cantidad"] -= cantidadMovimiento
                        break
                    else: 
                        print("Error: No hay suficientes existencias, el movimiento no se registro")
                        return False
        case _:
            print("Error: Tipo de movimiento erroneo")
            return False
        
    if encontrado == False:
        print("Error: No se encontro el producto solicitado")
        return False
    else:
        guardar_datos(datosMovimiento, "inventario", "movimientos")
        actualizar_datos(listaProductos, "inventario", "productos")
        print("Movimiento registrado con exito!")
        return True