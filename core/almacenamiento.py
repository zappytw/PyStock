import json

def cargarDatos(nombreArchivo):
    with open(f"data/{nombreArchivo}.json", "r", encoding="utf-8") as archivo:
        archivoCargado = json.load(archivo)

    return archivoCargado

def guardarDatos(datos, nombreArchivo):
    lista_datos = cargarDatos(nombreArchivo)
    lista_datos.append(datos)

    with open(f"data/{nombreArchivo}.json", "w", encoding="utf-8") as archivo:
        json.dump(lista_datos, archivo, indent=4, ensure_ascii=False)

