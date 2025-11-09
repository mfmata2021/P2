import socket

# IMPORTANTE RECORDAR!!!! El puerto y la ip se pide por linea de comandos, recordar cambiar !!!
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos el socket 
cliente.connect((socket.gethostname(), 5555)) #Lo conectamos a la dirección IP y al puerto 


# -- INICIO Y CONEXIÓN
"""El cliente pide el nombre de usuario y se conecta al servidor, enviando su 
credencial"""
while True:
    print("\n-- Bienvenido a la biblioteca de música --\n")
    print("Antes de iniciar, introduzca un nombre de usuario: ")
    usuario = input("> ")
    cliente.sendall(usuario.encode())
