import core
from core.almacenamiento import guardar_datos, cargar_datos

def registrar_producto(nombre, categoria, unidad, precio, cantidad, existencias_minimas):

    archivoProductos = cargar_datos("inventario", "productos")

    idMayor = 0
    for p in archivoProductos:
        if p["id"] > idMayor:
            idMayor = p["id"]

    idProducto = idMayor + 1

    datosProducto = {"id": idProducto, "nombre": nombre, "categoria": categoria, "unidad": unidad, "precio": precio, "cantidad": cantidad, "existencias_minimas": existencias_minimas, "activo":True}

    guardar_datos(datosProducto, "inventario", "productos")

    print("Producto agregado con exito!")

def nueva_categoria(nombreCategoria):
    lista_categorias = cargar_datos("inventario", "categorias")

    if nombreCategoria.lower() not in lista_categorias:
        lista_categorias.append(nombreCategoria.lower())
    else:
        print("Error: No se permiten duplicados, la categoria ya existe")

def nueva_unidad(nombreUnidad):
    lista_unidades = cargar_datos("inventario", "unidades")

    if nombreUnidad.lower() not in lista_unidades:
        lista_unidades.append(nombreUnidad.lower())
    else:
        print("Error: No se permiten duplicados, la unidad ya existe")