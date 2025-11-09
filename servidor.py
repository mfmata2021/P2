import socket
import threading


#Biblioteca que contendrá a los {"usuario" : usuario_socket} que se conecten al servidor y que no pueden ser usuados por nuevos clientes s
usuarios_activos = []
#Para poder modificar variables globales y evitar condiciones de carrera, usamos el lock 
lock = threading.Lock()

#IMPORTANTE RECORDAR!!!! EL puerto se pide por linea de comandos, recordar cambiar !!!
print("Arrancando servidor")
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((socket.gethostname(), 5555))
servidor.listen()

#Esta función es para comprobar si el usuario que ha escogido el cliente está disponible 
def comprobar_disponibilidad(u):
    if u not in usuarios_activos:
        usuarios_activos.append(u)
        return True
    return False 




def comunicacion (cliente, addr):
    if cliente:
        print(f"Cliente conectado en: {addr}")

        while True:
            usuario = cliente.recv(1024) #Aquí se recibiría el nombre de usuario de los clientes que se conectan
            if not usuario:
                print("Cerrando conexión")
                cliente.close()
                break 
            u = usuario.decode() #Aquí extraemos el nombre de usuario que ha elegido el cliente
            





#Esperamos a clientes infinitamente a menos que se interrumpa por teclado 
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
