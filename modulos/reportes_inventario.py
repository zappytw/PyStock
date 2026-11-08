from core.almacenamiento import cargar_datos


def reporte_existencias(usuarioActual):
    if usuarioActual == None:
        print("Error: Debe iniciar sesion")
        return

    productos = cargar_datos("inventario", "productos")

    print("\n--- EXISTENCIAS DEL INVENTARIO ---")
    for p in productos:
        if p["activo"] == True:
            print("ID:", p["id"], "| Producto:", p["nombre"],
                  "| Categoria:", p["categoria"], "| Cantidad:", p["cantidad"],
                  "| Minimo:", p["existencias_minimas"])


def reporte_alertas(usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede consultar las alertas")
        return

    productos = cargar_datos("inventario", "productos")
    hayAlertas = False

    print("\n--- ALERTAS DE INVENTARIO ---")
    for p in productos:
        if p["activo"] == True and p["cantidad"] <= p["existencias_minimas"]:
            print("Bajo inventario:", p["nombre"], "| Cantidad:", p["cantidad"],
                  "| Minimo:", p["existencias_minimas"])
            hayAlertas = True

    if hayAlertas == False:
        print("No hay alertas de inventario")
