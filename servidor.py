import socket
import threading
import pickle
import os
import json
from .datos_server import *
from herramientas_servidor import *


# Biblioteca que contendrá a los {"usuario" : usuario_socket} que se conecten al servidor y que no pueden ser usuados por nuevos clientes s
usuarios_activos = []
# Para poder modificar variables globales y evitar condiciones de carrera, usamos el lock
lock = threading.Lock()

# IMPORTANTE RECORDAR!!!! EL puerto se pide por linea de comandos, recordar cambiar !!!
print("\nArrancando servidor...")
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((socket.gethostname(), 5555))
servidor.listen()


def comunicacion (cliente, addr):

    global usuarios_activos

    if cliente:
        print(f"Cliente conectado en: {addr}")

        while True:
            # -- Envío al cliente la lista de usuarios activos en el servidor

            # IMPORTANTE:Si un hilo puede modificar la lista, entonces todas las lecturas deben protegerse también
            try: 
                lock.acquire()
                data = pickle.dumps(usuarios_activos)
            finally:
                lock.release()
            cliente.sendall(data)

            # -- Nos "comunicamos" con el cliente por medio de comandos, dependiendo de lo que nos diga, vamos haciendo x tareas en el servidor

            mensaje = cliente.recv(1024).decode() #Aquí llegaría el comando 
            comando = mensaje.split(":")

            if comando[0] == "REGISTRO":
                usuario = comando[1]
                try:
                    lock.acquire()
                    if usuario not in usuarios_activos:
                        usuarios_activos.append(usuario)
                        crear_carpeta(usuario)
                        respuesta = 'OK'
                    
                    else:
                        respuesta = "DENEGADO"
                finally:
                    lock.release()
                cliente.sendall(respuesta.encode())

    
            # ------------------ SINCRONIZACIÓN INICIAL Y DESCARGA ---------------------------
            elif comando[0] == "SYNC_INICIO":
                pass


# Esperamos a clientes infinitamente a menos que se interrumpa por teclado
try:
    while True: 
        # Espera a que llegue un nuevo cliente
        cliente, addr = servidor.accept() 


        # Establecida la conexión, crear un objeto hilo para atender al cliente
        # - target: nombre de la función que ejecuta el hilo (sin paréntesis)
        # - args: tupla con los argumentos de la función     
        hilo = threading.Thread(target=comunicacion, args=(cliente, addr))

        #Lanzar el hilo
        hilo.start()

except KeyboardInterrupt:  # Captura la señal generada por Ctrl+C
    servidor.close()  # Cierra el socket del servidor
    print("Apagando servidor...")
