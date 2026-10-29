import json

def cargar_datos(nombreCarpeta, nombreArchivo):
    with open(f"data/{nombreCarpeta}/{nombreArchivo}.json", "r", encoding="utf-8") as archivo:
        archivoCargado = json.load(archivo)

    return archivoCargado

def guardar_datos(datos, nombreCarpeta, nombreArchivo):
    lista_datos = cargar_datos(nombreCarpeta, nombreArchivo)
    lista_datos.append(datos)

    with open(f"data/{nombreCarpeta}/{nombreArchivo}.json", "w", encoding="utf-8") as archivo:
        json.dump(lista_datos, archivo, indent=4, ensure_ascii=False)

