import socket
import threading

# Key-Value store condiviso tra tutte le connessioni
kv_store = {}
store_lock = threading.Lock()


def process_line(line):
    # Rimuove eventuali spazi o caratteri di newline finali (\r o \n)
    line = line.rstrip("\n")
    if not line:
        return None

    # Separa il comando dal resto della riga basandosi sul primo spazio
    parts = line.split(" ", 1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    #Comando PING
    if cmd == "PING":
        return "PONG"

    #Comando ECHO
    elif cmd == "ECHO":
        return args  # Restituisce tutto quello che segue il primo spazio

    #Comando SET
    elif cmd == "SET":
        # Separa la chiave dal valore (la chiave non contiene spazi)
        kv_parts = args.split(" ", 1)
        if len(kv_parts) < 2:  # SET senza un valore -> ERR
            return "ERR"
        key, value = kv_parts[0], kv_parts[1]

        with store_lock:
            kv_store[key] = value
        return "OK"

    # 4. Comando GET
    elif cmd == "GET":
        if not args or " " in args:  # GET senza chiave o con più parole
            return "ERR"
        key = args

        with store_lock:
            if key in kv_store:
                return kv_store[key]
            else:
                return "NOT_FOUND"

    # Comando sconosciuto
    else:
        return "ERR"


def handle_client(client_socket):
    buffer = ""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # Il client ha chiuso la connessione

            buffer += data.decode("ascii", errors="replace")

            # Gestione framing: processa tutte le righe complete terminate da \n
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                response = process_line(line)
                if response is not None:
                    client_socket.sendall((response + "\n").encode("ascii"))

    except Exception:
        pass
    finally:
        client_socket.close()


def start_server(host="0.0.0.0", port=9001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permette il riutilizzo immediato della porta
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server TCP in ascolto sulla porta {port}...")

    while True:
        client_socket, _ = server_socket.accept()
        # Gestisce ogni client in un thread separato per la concorrenza
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket,)
        )
        client_thread.daemon = True
        client_thread.start()


if __name__ == "__main__":
    start_server()