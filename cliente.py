import socket
import pickle
from herramientas_cliente import *

# IMPORTANTE RECORDAR!!!! El puerto y la ip se pide por linea de comandos, recordar cambiar !!!
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos el socket 
cliente.connect((socket.gethostname(), 5555)) #Lo conectamos a la dirección IP y al puerto 


"""El cliente pide el nombre de usuario y se conecta al servidor, enviando su 
credencial"""


# Lista de usuarios que tiene el servidor conectado, así podemos comprobar que no se repita el mismo nombre
data = cliente.recv(1024)
usuarios_bloqueados = pickle.loads(data) #Aquí está la lista de usuarios bloqueados que tiene el servidor 

print("\n-- Bienvenido a la biblioteca de música --\n")
print("Antes de iniciar, introduzca un nombre de usuario")

# ------------ INICIO Y CONEXIÓN -------------------------------------
# Bucle para comprobar que no se repita el mismo nombre de usuario
while True: 
    usuario = input("> ").strip()

    if not usuario:
        print("El nombre no puede estar vacío")
        continue

    if usuario not in usuarios_bloqueados:
        comando = "REGISTRO"
        mensaje = comando + ":" + usuario
        cliente.sendall(mensaje.encode())
        break
    else:
        print("El nombre de usuario no está disponible. Inténtelo de nuevo")
        
respuesta = cliente.recv(1024).decode()
if respuesta == "OK":
        print("Usuario conectado")
else:
    print("Registro rechazado por el servidor")
    cliente.close()
    exit()

# ---------- SINCRONIZACIÓN INICIAL Y DESCARGA --------------------------
comando = "SINCRONIZAR"
cliente.sendall(comando.encode()) #Si el servidor responde que OK, el cliente solicita la descarga de su biblioteca
print("\nDescargando biblioteca...\n")
data_json = recibir_json(cliente, usuario)
recibir_mp3(cliente, usuario)
print("Biblioteca descargada y lista para usar")

# ------------- TRABAJO LOCAL -----------------------
plataforma = reconstruir_plataforma(usuario, data_json)

# -------------- CIERRE Y SINCRONIZACIÓN FINAL -------------
cliente.sendall("SUBIR".encode())
enviar_json(cliente, usuario)
enviar_mp3(cliente, usuario)

cliente.sendall("SALIR".encode())
cliente.close()
