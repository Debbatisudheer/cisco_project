import socket
import threading
import json
from search import Search


def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    data = json.loads(request)

    filename = data.get('filename')
    word = data.get('word')

    try:
        search_obj = Search(filename)
        search_obj.clean()
        result = search_obj.getLines(word)
        response = json.dumps(result)
    except Exception as e:
        response = json.dumps({'error': str(e)})

    client_socket.send(response.encode('utf-8'))
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999...")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
