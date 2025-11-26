import os 
import json 


# Esta función, creará un nuevo directorio para cada usuario nuevo que se conecte
def crear_carpeta(nombre_usuario):
    ruta = os.path.join("datos_server", nombre_usuario)

    try:
        os.mkdir(ruta)
        print(f"Carpeta creada: {ruta}")
    except FileExistsError:
        print(f"La carpeta ya existe: {ruta}")

    return ruta


def leer_carpeta():
    pass
