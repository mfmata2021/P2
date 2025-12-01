import os 
import json
from plataforma import PlataformaMusical, Cancion, ListaReproduccion


def recibir_json(cliente, usuario):
    # Recibir tamaño del JSON
    tamaño = int(cliente.recv(1024).decode())

    # Recibir contenido del JSON
    recibido = b""
    while len(recibido) < tamaño:
        chunk = cliente.recv(1024)
        recibido += chunk

    # Convertir de bytes a texto
    texto = recibido.decode()

    # Guardar localmente
    ruta_local = os.path.join("datos_cliente", usuario)
    if not os.path.exists(ruta_local):
        os.makedirs(ruta_local)
    with open(os.path.join(ruta_local, "biblioteca.json"), "w") as f:
        f.write(texto)

    # Devolver contenido JSON como dict

    return json.loads(texto)


def recibir_mp3(cliente, usuario):
    # Carpeta local donde guardar mp3
    carpeta = os.path.join("datos_cliente", usuario, "mp3")
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Recibir número de archivos
    num_archivos = int(cliente.recv(1024).decode())

    for _ in range(num_archivos):
        # Recibir tamaño del archivo
        tamaño = int(cliente.recv(1024).decode())

        # Recibir nombre del archivo
        nombre = cliente.recv(1024).decode()

        # Recibir datos
        recibido = b""
        while len(recibido) < tamaño:
            chunk = cliente.recv(1024)
            recibido += chunk

        # Guardar archivo
        with open(os.path.join(carpeta, nombre), "wb") as f:
            f.write(recibido)


def enviar_json(cliente, usuario):
    ruta = os.path.join("datos_cliente", usuario, "biblioteca.json")
    with open(ruta, "r") as f:
        texto = f.read()

    cliente.sendall(str(len(texto)).encode())
    cliente.sendall(b"\n")
    cliente.sendall(texto.encode())


def enviar_mp3(cliente, usuario):
    carpeta = os.path.join("datos_cliente", usuario, "mp3")
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".mp3")]

    # Número de archivos
    cliente.sendall(str(len(archivos)).encode())
    cliente.sendall(b"\n")

    for nombre in archivos:
        ruta = os.path.join(carpeta, nombre)
        with open(ruta, "rb") as f:
            datos = f.read()

        cliente.sendall(str(len(datos)).encode())
        cliente.sendall(b"\n")

        cliente.sendall(nombre.encode())
        cliente.sendall(b"\n")

        cliente.sendall(datos)


def reconstruir_plataforma(usuario, data_json):
    plataforma = PlataformaMusical()

    # Reconstruir canciones
    for c in data_json["canciones"]:
        ruta_archivo = os.path.join("datos_cliente", usuario, c["archivo"])
        cancion = Cancion(
            c["id"], c["titulo"], c["artista"], c["duracion"], c["genero"], ruta_archivo
        )
        plataforma.canciones.append(cancion)

    # Reconstruir listas
    for l in data_json["listas"]:
        lista = ListaReproduccion(l["nombre"])
        lista.canciones = l["canciones"]
        plataforma.listas.append(lista)

    return plataforma
