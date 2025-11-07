import socket
import threading



print("Arrancando servidor")
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((socket.gethostname(), 5555))
servidor.listen()


def comunicacion (cliente, addr):
    if cliente:
        print(f"Cliente conectado en: {addr}")

        while True:
            usuario = cliente.recv(1024) #Aquí se recibiría el nombre de usuario de los clientes que se conectan
            if not usuario:
                print("Cerrando conexión")
                cliente.close()
                break 



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
