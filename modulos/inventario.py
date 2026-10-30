import core
from core.almacenamiento import guardar_datos, cargar_datos, actualizar_datos

def registrar_producto(nombre, categoria, unidad, precio, cantidad, existencias_minimas):

    archivoProductos = cargar_datos("inventario", "productos")

    idMayor = 0
    for p in archivoProductos:
        if p["id"] > idMayor:
            idMayor = p["id"]
    
    idProducto = idMayor + 1

    datosProducto = {"id": idProducto, "nombre": nombre, "categoria": categoria,
                    "unidad": unidad, "precio": precio, "cantidad": cantidad, 
                    "existencias_minimas": existencias_minimas, "activo":True}

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

def editar_producto(idProducto, dato, nuevoValor):
    archivoProductos = cargar_datos("inventario", "productos")
    encontrado = False
    for p in archivoProductos:
        if p["id"] == idProducto:
            if dato in p:
                p[dato] = nuevoValor
                encontrado = True
                break
            else:
                print("Error: El dato que intenta modificar no existe")
                return
    if encontrado == False:
        print("Error: No se encontro el producto solicitado")
    else:
        actualizar_datos(archivoProductos, "inventario", "productos")
        print("Dato actualizado con exito!")

##Paso 5: Consulta, modificación y desactivación (RF 6)

#Consultar, editar datos y precios, y desactivar productos sin borrar su historial.