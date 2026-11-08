from core.almacenamiento import cargar_datos, guardar_datos, actualizar_datos
import os
import shutil
from datetime import datetime


def existe_propietario():
    listaUsuarios = cargar_datos("Usuarios", "Usuarios")

    for u in listaUsuarios:
        if u["rol"] == "propietario":
            return True

    return False


def registrar_propietario(nombre, nombreUsuario, contrasena):
    listaUsuarios = cargar_datos("Usuarios", "Usuarios")

    if existe_propietario() == True:
        print("Error: Ya existe un propietario registrado")
        return

    if nombre == "" or nombreUsuario == "" or contrasena == "":
        print("Error: Todos los campos son obligatorios")
        return

    if len(contrasena) < 8:
        print("Error: La contrasena debe tener minimo 8 caracteres")
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
        "rol": "propietario",
        "activo": True
    }

    guardar_datos(datosUsuario, "Usuarios", "Usuarios")
    print("Propietario registrado con exito!")


def registrar_usuario(nombre, nombreUsuario, contrasena, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede registrar empleados")
        return

    listaUsuarios = cargar_datos("Usuarios", "Usuarios")

    if nombre == "" or nombreUsuario == "" or contrasena == "":
        print("Error: Todos los campos son obligatorios")
        return

    if len(contrasena) < 8:
        print("Error: La contrasena debe tener minimo 8 caracteres")
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
        "rol": "empleado",
        "activo": True
    }

    guardar_datos(datosUsuario, "Usuarios", "Usuarios")
    print("Empleado registrado con exito!")


def iniciar_sesion(nombreUsuario, contrasena):
    listaUsuarios = cargar_datos("Usuarios", "Usuarios")

    for u in listaUsuarios:
        if u["nombreUsuario"].lower() == nombreUsuario.lower():
            if u["activo"] == False:
                print("Error: El usuario esta desactivado")
                return None

            if u["contrasena"] == contrasena:
                print("Inicio de sesion exitoso!")
                usuarioActual = {
                    "id": u["id"],
                    "nombre": u["nombre"],
                    "nombreUsuario": u["nombreUsuario"],
                    "rol": u["rol"]
                }
                return usuarioActual
            else:
                print("Error: Contrasena incorrecta")
                return None

    print("Error: Usuario no encontrado")
    return None


def cerrar_sesion(usuarioActual):
    if usuarioActual == None:
        print("No hay una sesion activa")
        return None

    print("Sesion cerrada")
    return None


def consultar_usuarios(usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para consultar usuarios")
        return

    listaUsuarios = cargar_datos("Usuarios", "Usuarios")

    for u in listaUsuarios:
        print("ID:", u["id"], "| Nombre:", u["nombre"],
              "| Usuario:", u["nombreUsuario"], "| Rol:", u["rol"],
              "| Activo:", u["activo"])


def editar_usuario(idUsuario, nuevoNombre, nuevoNombreUsuario, nuevaContrasena, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para editar usuarios")
        return

    listaUsuarios = cargar_datos("Usuarios", "Usuarios")
    encontrado = False

    for u in listaUsuarios:
        if u["id"] == idUsuario:
            if u["rol"] == "propietario":
                print("Error: No se puede editar al propietario")
                return

            if nuevoNombre == "" or nuevoNombreUsuario == "":
                print("Error: Los campos son obligatorios")
                return

            for otroUsuario in listaUsuarios:
                if otroUsuario["nombreUsuario"].lower() == nuevoNombreUsuario.lower():
                    if otroUsuario["id"] != idUsuario:
                        print("Error: El nombre de usuario ya existe")
                        return

            if nuevaContrasena != "":
                if len(nuevaContrasena) < 8:
                    print("Error: La contrasena debe tener minimo 8 caracteres")
                    return
                u["contrasena"] = nuevaContrasena

            u["nombre"] = nuevoNombre
            u["nombreUsuario"] = nuevoNombreUsuario
            encontrado = True
            break

    if encontrado == False:
        print("Error: No se encontro el empleado")
    else:
        actualizar_datos(listaUsuarios, "Usuarios", "Usuarios")
        print("Usuario actualizado con exito!")


def eliminar_usuario(idUsuario, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: No tiene permisos para desactivar usuarios")
        return

    listaUsuarios = cargar_datos("Usuarios", "Usuarios")
    encontrado = False

    for u in listaUsuarios:
        if u["id"] == idUsuario:
            if u["rol"] == "propietario":
                print("Error: No se puede desactivar al propietario")
                return
            u["activo"] = False
            encontrado = True
            break

    if encontrado == False:
        print("Error: No se encontro el empleado")
    else:
        actualizar_datos(listaUsuarios, "Usuarios", "Usuarios")
        print("Empleado desactivado con exito!")


def crear_copia_seguridad():
    os.makedirs("copias_seguridad", exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    carpeta = "copias_seguridad/copia_" + fecha
    os.makedirs(carpeta)
    shutil.copytree("data/Usuarios", carpeta + "/Usuarios")
    shutil.copytree("data/abastecimiento", carpeta + "/abastecimiento")
    print("Copia de seguridad creada:", carpeta)


def restaurar_copia_seguridad(ruta, usuarioActual):
    if usuarioActual == None or usuarioActual["rol"] != "propietario":
        print("Error: Solo el propietario puede restaurar una copia")
        return

    if os.path.exists(ruta + "/Usuarios/Usuarios.json") == False:
        print("Error: No se encontro la copia de usuarios")
        return

    if os.path.exists(ruta + "/abastecimiento") == False:
        print("Error: No se encontro la copia de abastecimiento")
        return

    shutil.rmtree("data/Usuarios")
    shutil.copytree(ruta + "/Usuarios", "data/Usuarios")
    shutil.rmtree("data/abastecimiento")
    shutil.copytree(ruta + "/abastecimiento", "data/abastecimiento")
    print("Copia restaurada. Los datos de inventario de Persona A no fueron modificados")
