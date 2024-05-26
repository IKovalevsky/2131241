import multiprocessing as mp
import socket

def listen_tcp_service(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        print(f"[+] Connecting to {host}:{port}...")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode('utf-8').strip())

    except (ConnectionRefusedError, ConnectionResetError, socket.error) as e:
        print(e)

    finally:
        client_socket.close()
        print(f"[!] {host}:{port} - connection dropped.")

def main():
    host = '127.0.0.1'
    ports = [10000, 10001]
    processes = []

    for port in ports:
        process = mp.Process(target=listen_tcp_service, args=(host, port))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == '__main__':
    main()
