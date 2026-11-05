
from core.almacenamiento import cargar_datos, guardar_datos, actualizar_datos


def registrar_usuario(nombre, nombreUsuario, contrasena, rol):

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    if nombre == "" or nombreUsuario == "" or contrasena == "":
        print("Error: Todos los campos son obligatorios")
        return

    if rol != "propietario" and rol != "empleado":
        print("Error: El rol ingresado no es valido")
        return

    for u in listaUsuarios:
        if u["nombreUsuario"].lower() == nombreUsuario.lower():
            print("Error: El nombre de usuario ya existe")
            return

    idMayor = 0

    for u in listaUsuarios:
        if u["id"] > idMayor:
            idMayor = u["id"]

    datosUsuario = {
        "id": idMayor + 1,
        "nombre": nombre,
        "nombreUsuario": nombreUsuario,
        "contrasena": contrasena,
        "rol": rol,
        "activo": True
    }

    guardar_datos(datosUsuario, "usuarios", "usuarios")
    print("Usuario registrado con exito!")


def iniciar_sesion(nombreUsuario, contrasena):

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    for u in listaUsuarios:

        if u["nombreUsuario"] == nombreUsuario:

            if u["contrasena"] == contrasena:

                if u["activo"] == True:
                    print("Inicio de sesion exitoso!")
                    return u

                else:
                    print("Error: El usuario esta desactivado")
                    return None

            else:
                print("Error: Contrasena incorrecta")
                return None

    print("Error: Usuario no encontrado")
    return None


def consultar_usuarios():

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    for u in listaUsuarios:
        print(
            "ID:", u["id"],
            "| Nombre:", u["nombre"],
            "| Usuario:", u["nombreUsuario"],
            "| Rol:", u["rol"],
            "| Activo:", u["activo"]
        )


def cambiar_estado_usuario(idUsuario, nuevoEstado):

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    encontrado = False

    for u in listaUsuarios:

        if u["id"] == idUsuario:

            u["activo"] = nuevoEstado
            encontrado = True
            break

    if encontrado == False:
        print("Error: No se encontro el usuario")

    else:
        actualizar_datos(listaUsuarios, "usuarios", "usuarios")
        print("Estado del usuario actualizado con exito!")
