import socket
import pickle

# IMPORTANTE RECORDAR!!!! El puerto y la ip se pide por linea de comandos, recordar cambiar !!!
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos el socket 
cliente.connect((socket.gethostname(), 5555)) #Lo conectamos a la dirección IP y al puerto 


"""El cliente pide el nombre de usuario y se conecta al servidor, enviando su 
credencial"""
while True:

    # Lista de usuarios que tiene el servidor conectado, así podemos comprobar que no se repita el mismo nombre
    data = cliente.recv(1024)
    usuarios_bloqueados = pickle.loads(data) #Aquí está la lista de usuarios bloqueados que tiene el servidor 

    print("\n-- Bienvenido a la biblioteca de música --\n")
    print("Antes de iniciar, introduzca un nombre de usuario")

    # -- INICIO Y CONEXIÓN
    # Bucle para comprobar que no se repita el mismo nombre de usuario
    while True: 
        usuario = input("> ")
        if usuario not in usuarios_bloqueados:
            cliente.sendall(usuario.encode())
            break
        else:
            print("El nombre de usuario no está disponible. Inténtelo de nuevo")

    # -- SINCRONIZACIÓN INICIAL Y DESCARGA
    
    # -- TRABAJO LOCAL

    # -- CIERRE Y SINCRONIZACIÓN FINAL
