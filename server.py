import socket
import threading

# Lista global para almacenar los sockets de los clientes conectados
clients = []

def handle_client(client_socket, addr):
    """Maneja la comunicación con un cliente."""
    print(f"Cliente {addr} conectado.")
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                decoded_message = message.decode('utf-8')
                print(f"Mensaje de {addr}: {decoded_message}")
                broadcast(message, client_socket)
            else:
                # Si no se recibe mensaje, se asume que el cliente se desconectó
                remove_client(client_socket, addr)
                break
        except Exception as e:
            print(f"Error con {addr}: {e}")
            remove_client(client_socket, addr)
            break

def broadcast(message, sender_socket):
    """Envía el mensaje a todos los clientes conectados excepto al que lo envió."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error al enviar mensaje a un cliente: {e}")
                remove_client(client, "desconocido")

def remove_client(client_socket, addr):
    """Elimina el socket de cliente y lo cierra."""
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()
        print(f"Cliente {addr} desconectado.")

def main():
    # Crea un socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Vincula el socket a todas las interfaces en el puerto 5000
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("Servidor escuchando en el puerto 5000...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        # Crea un hilo para manejar la comunicación con el cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
