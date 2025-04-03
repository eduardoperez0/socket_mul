import socket
import threading

def receive_messages(client_socket):
    """Escucha y muestra los mensajes que llegan del servidor."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print("\nMensaje recibido:", message.decode('utf-8'))
            else:
                print("Servidor desconectado.")
                break
        except Exception as e:
            print(f"Error al recibir mensajes: {e}")
            break

def main():
    # Crea el socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Ingresa la IP del servidor (asegúrate de que sea accesible para todos los dispositivos)
    server_ip = input("Ingresa la IP del servidor: ")
    try:
        client_socket.connect((server_ip, 5000))
        print("Conectado al servidor.")
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
        return
    
    # Inicia un hilo para recibir mensajes
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True
    thread.start()

    # Enviar mensajes al servidor
    while True:
        message = input()
        if message.lower() == "salir":
            print("Cerrando conexión...")
            client_socket.close()
            break
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break

if __name__ == "__main__":
    main()
