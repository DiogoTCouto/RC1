import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(f'starting up on {server_address}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

total_bytes_received = 0

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print(f'connection from {client_address}')

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data:
                total_bytes_received += len(data)
                print(f'received {data}')
                response = f'Hostname: {socket.gethostname()}\n' \
                           f'IP address: {socket.gethostbyname(socket.gethostname())}\n' \
                           f'Total bytes received: {total_bytes_received}'
                connection.sendall(response.encode())
            else:
                print('no more data from', client_address)
                break
    finally:
        # Clean up the connection
        connection.close()
