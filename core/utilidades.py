
def Campo_vacio(dato):
    if dato.strip() == "":
        return False
    else:
        return True


def buscar_usuario(listaUsuarios, nombreUsuario):

    encontrado = False

    for u in listaUsuarios:
        if u["nombreUsuario"].lower() == nombreUsuario.lower():
            encontrado = True
            return u

    return None


def obtener_id_mayor(listaDatos):

    idMayor = 0

    for dato in listaDatos:
        if dato["id"] > idMayor:
            idMayor = dato["id"]

    return idMayor
