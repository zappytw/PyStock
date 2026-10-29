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

                    if p["cantidad"] - cantidadMovimiento >= 0:
                        p["cantidad"] -= cantidadMovimiento
                        break
                    else: 
                        print("Error: No hay suficientes existencias, el movimiento no se registro")
                        return
        case _:
            print("Error: Tipo de movimiento erroneo")
            return
        
    if encontrado == False:
        print("Error: No se encontro el producto solicitado")
    else:
        guardar_datos(datosMovimiento, "inventario", "movimientos")
        actualizar_datos(listaProductos, "inventario", "productos")
        print("Movimiento registrado con exito!")