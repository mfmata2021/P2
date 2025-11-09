import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos el socket 
cliente.connect((socket.gethostname(), 5555)) #Lo conectamos a la dirección IP y al puerto 

#-- INICIO Y CONEXIÓN 