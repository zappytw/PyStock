
from core.almacenamiento import cargar_datos, guardar_datos, actualizar_datos
import hashlib
import secrets
import hmac


def generar_contrasena(contrasena, salt=None):
    """Genera un hash seguro de la contraseña."""
    if salt is None:
        salt = secrets.token_hex(16)

    hash_contrasena = hashlib.pbkdf2_hmac(
        "sha256",
        contrasena.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    ).hex()

    return salt, hash_contrasena


def registrar_usuario(nombre, nombre_usuario, contrasena, rol):
    """Registra un propietario o empleado."""

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    if not nombre.strip() or not nombre_usuario.strip():
        print("Error: El nombre y usuario son obligatorios")
        return

    if len(contrasena) < 8:
        print("Error: La contraseña debe tener al menos 8 caracteres")
        return

    if rol not in ["propietario", "empleado"]:
        print("Error: El rol debe ser propietario o empleado")
        return

    for u in listaUsuarios:
        if u["nombre_usuario"].lower() == nombre_usuario.lower():
            print("Error: El nombre de usuario ya existe")
            return

    idMayor = 0

    for u in listaUsuarios:
        if u["id"] > idMayor:
            idMayor = u["id"]

    salt, hash_contrasena = generar_contrasena(contrasena)

    nuevoUsuario = {
        "id": idMayor + 1,
        "nombre": nombre.strip(),
        "nombre_usuario": nombre_usuario.strip(),
        "contrasena_hash": hash_contrasena,
        "salt": salt,
        "rol": rol,
        "activo": True
    }

    guardar_datos(nuevoUsuario, "usuarios", "usuarios")

    print("Usuario registrado con éxito!")


def iniciar_sesion(nombre_usuario, contrasena):
    """Verifica las credenciales e inicia sesión."""

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    for u in listaUsuarios:

        if u["nombre_usuario"].lower() == nombre_usuario.lower():

            if not u["activo"]:
                print("Error: El usuario está desactivado")
                return None

            salt, hash_contrasena = generar_contrasena(
                contrasena,
                u["salt"]
            )

            if hmac.compare_digest(
                hash_contrasena,
                u["contrasena_hash"]
            ):
                print("Inicio de sesión exitoso!")

                return {
                    "id": u["id"],
                    "nombre": u["nombre"],
                    "nombre_usuario": u["nombre_usuario"],
                    "rol": u["rol"]
                }

            print("Error: Contraseña incorrecta")
            return None

    print("Error: El usuario no existe")
    return None


def consultar_usuarios():
    """Devuelve la lista de usuarios sin mostrar sus contraseñas."""

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    usuarios = []

    for u in listaUsuarios:
        usuarios.append({
            "id": u["id"],
            "nombre": u["nombre"],
            "nombre_usuario": u["nombre_usuario"],
            "rol": u["rol"],
            "activo": u["activo"]
        })

    return usuarios


def cambiar_estado_usuario(id_usuario, nuevo_estado):
    """Activa o desactiva un usuario."""

    if not isinstance(nuevo_estado, bool):
        print("Error: El estado debe ser True o False")
        return

    listaUsuarios = cargar_datos("usuarios", "usuarios")

    for u in listaUsuarios:
        if u["id"] == id_usuario:
            u["activo"] = nuevo_estado

            actualizar_datos(
                listaUsuarios,
                "usuarios",
                "usuarios"
            )

            print("Estado del usuario actualizado!")
            return

    print("Error: No se encontró el usuario")
