from core.almacenamiento import guardar_datos, cargar_datos, actualizar_datos

def registrar_producto(nombre, categoria, unidad, precio, cantidad, existencias_minimas):
    archivoProductos = cargar_datos("inventario", "productos")
    archivoCategorias = cargar_datos("inventario", "categorias")
    archivoUnidades = cargar_datos("inventario", "unidades")

    if unidad.lower().strip() not in archivoUnidades or categoria.lower().strip() not in archivoCategorias:
        print("ERROR: La categoria o unidad proporcionada no existe, por favor revisar las categorias y unidades existentes")
        return False
    
    idMayor = 0
    for p in archivoProductos:
        if p["id"] > idMayor:
            idMayor = p["id"]
    
    idProducto = idMayor + 1

    datosProducto = {"id": idProducto, "nombre": nombre.lower(), "categoria": categoria.lower(),
                    "unidad": unidad.lower(), "precio": precio, "cantidad": cantidad, 
                    "existencias_minimas": existencias_minimas, "activo":True}

    guardar_datos(datosProducto, "inventario", "productos")
    print("Producto agregado con exito!")



def nueva_categoria(nombreCategoria):
    lista_categorias = cargar_datos("inventario", "categorias")

    if nombreCategoria.lower() not in lista_categorias:
        guardar_datos(nombreCategoria.lower(), "inventario", "categorias")

    else:
        print("Error: No se permiten duplicados, la categoria ya existe")



def nueva_unidad(nombreUnidad):
    lista_unidades = cargar_datos("inventario", "unidades")

    if nombreUnidad.lower() not in lista_unidades:
        guardar_datos(nombreUnidad.lower(), "inventario", "unidades")
    else:
        print("Error: No se permiten duplicados, la unidad ya existe")



def editar_producto(idProducto, dato_a_editar, nuevoValor):
    archivoProductos = cargar_datos("inventario", "productos")
    encontrado = False
    for p in archivoProductos:
        if p["id"] == idProducto:
            if dato_a_editar.lower() in p:
                p[dato_a_editar.lower()] = nuevoValor.lower().strip() if type(nuevoValor) == str else nuevoValor.strip()
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

def cargar_productos(atributoABuscar, busqueda=""):
    lista_productos = cargar_datos("inventario", "productos")
    productos_filtrados = []

    for p in lista_productos:
        if busqueda.lower() in p[atributoABuscar] and p["activo"]:
            productos_filtrados.append(p)

    return productos_filtrados

def obtener_producto(id_producto):
    for p in cargar_datos("inventario", "productos"):
        if p["id"] == id_producto and p["activo"]:
            return p
    return None

