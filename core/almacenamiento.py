import json

def cargar_datos(nombreCarpeta, nombreArchivo):
    with open(f"data/{nombreCarpeta}/{nombreArchivo}.json", "r", encoding="utf-8") as archivo:
        archivoCargado = json.load(archivo)

    return archivoCargado

def guardar_datos(nuevoRegistro, nombreCarpeta, nombreArchivo):
    lista_datos = cargar_datos(nombreCarpeta, nombreArchivo)
    lista_datos.append(nuevoRegistro)

    actualizar_datos(lista_datos, nombreCarpeta, nombreArchivo)

def actualizar_datos(datos, nombreCarpeta, nombreArchivo):
    with open(f"data/{nombreCarpeta}/{nombreArchivo}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)