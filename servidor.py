import socket
import threading
import pickle
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
    usuario = None

    if cliente:
        print(f"Cliente conectado en: {addr}")
        # -- Envío al cliente la lista de usuarios activos en el servidor
        lock.acquire()
        data = pickle.dumps(usuarios_activos)
        lock.release()
        cliente.sendall(data)


        try:
            while True:

                # IMPORTANTE:Si un hilo puede modificar la lista, entonces todas las lecturas deben protegerse también

                # -- Nos "comunicamos" con el cliente por medio de comandos, dependiendo de lo que nos diga, vamos haciendo x tareas en el servidor

                mensaje = cliente.recv(1024) #Aquí llegaría el comando 
                if not mensaje:
                    break

                comando = mensaje.decode().split(":")

                if comando[0] == "REGISTRO":
                    usuario = comando[1]

                    lock.acquire()
                    try:
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
                elif comando[0] == "SINCRONIZAR" and usuario:

                    enviar_json(cliente, usuario)
                    enviar_mp3(cliente, usuario)

                elif comando[0] == "SUBIR" and usuario:

                    recibir_json(cliente, usuario)
                    recibir_mp3(cliente, usuario)

                elif comando[0] == "SALIR":
                    break  # Salir del bucle del hilo

        finally:
            if usuario:
                lock.acquire()
                if usuario in usuarios_activos:
                    usuarios_activos.remove(usuario)
                lock.release()
            cliente.close()
            print(f"Usuario {usuario} liberado y conexión cerrada")
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
