import os 


# Esta función, creará un nuevo directorio para cada usuario nuevo que se conecte
def crear_carpeta(nombre_usuario):
    ruta_usuario = os.path.join("datos_server", nombre_usuario)
    ruta_mp3 = os.path.join(ruta_usuario, "mp3")

    os.makedirs(ruta_mp3, exist_ok=True)
    print(f"Carpetas creadas: {ruta_usuario} / mp3")


def enviar_json(cliente, usuario):

    ruta = os.path.join("datos_server", usuario, "biblioteca.json")

    # Si no existe, crear JSON vacío
    if not os.path.exists(ruta):
        with open(ruta, "w") as f:
            f.write('{"canciones": [], "listas": []}')


    # Leer el contenido del archivo
    with open(ruta, "r") as f:
        texto = f.read()


    # Enviar el tamaño del JSON
    cliente.sendall(str(len(texto)).encode())
    cliente.sendall(b"\n")

    # Enviar el contenido
    cliente.sendall(texto.encode())


def enviar_mp3(cliente, usuario):

    carpeta = os.path.join("datos_server", usuario, "mp3")

    # Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.mkdir(carpeta)

    # Contar mp3
    archivos = []

    for nombre in os.listdir(carpeta):  # archivos será una lista de strings, donde cada string es el nombre de un archivo o subcarpeta dentro de "mi_carpeta"
        if nombre.endswith(".mp3"):
            archivos.append(nombre)

    # Enviar cuántos mp3 hay
    cliente.sendall(str(len(archivos)).encode())
    cliente.sendall(b"\n")

    # Enviar cada mp3
    for nombre in archivos:
        ruta = os.path.join(carpeta, nombre)

        with open(ruta, "rb") as f:
            datos = f.read()

        # Tamaño del archivo
        cliente.sendall(str(len(datos)).encode())
        cliente.sendall(b"\n")

        # Nombre del archivo
        cliente.sendall(nombre.encode())
        cliente.sendall(b"\n")

        # Datos binarios
        cliente.sendall(datos)


def recibir_json(cliente, usuario):
    # Recibir tamaño del JSON
    tamaño = int(cliente.recv(1024).decode())
    cliente.recv(1)  # Saltamos el '\n'

    # Recibir contenido del JSON
    recibido = b""
    while len(recibido) < tamaño:
        recibido += cliente.recv(1024)

    # Guardar JSON en servidor
    ruta = os.path.join("datos_server", usuario, "biblioteca.json")
    with open(ruta, "w") as f:
        f.write(recibido.decode())


def recibir_mp3(cliente, usuario):
    carpeta = os.path.join("datos_server", usuario, "mp3")
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Número de archivos
    num_archivos = int(cliente.recv(1024).decode())
    cliente.recv(1)  # Saltamos '\n'

    for _ in range(num_archivos):
        # Tamaño del archivo
        tamaño = int(cliente.recv(1024).decode())
        cliente.recv(1)

        # Nombre del archivo
        nombre = cliente.recv(1024).decode()
        cliente.recv(1)

        # Recibir datos
        recibido = b""
        while len(recibido) < tamaño:
            recibido += cliente.recv(1024)

        # Guardar archivo
        ruta_archivo = os.path.join(carpeta, nombre)
        with open(ruta_archivo, "wb") as f:
            f.write(recibido)
