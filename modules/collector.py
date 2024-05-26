import multiprocessing as mp
import socket

class LogListener:
    def __init__(self, queue):
        self.queue = queue

    def listen_tcp_service(self, host, port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            print(f"[+] Connecting to {host}:{port}...")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                log_string = data.decode('utf-8').strip()
                print(log_string)
                self.queue.put(log_string)

        except (ConnectionRefusedError, ConnectionResetError, socket.error) as e:
            print(e)

        finally:
            client_socket.close()
            print(f"[!] {host}:{port} - connection dropped.")

    def start(self, host, ports):
        processes = []
        for port in ports:
            process = mp.Process(target=self.listen_tcp_service, args=(host, port))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

if __name__ == '__main__':
    queue = mp.Queue()
    listener = LogListener(queue)
    listener.start('127.0.0.1', [10000, 10001])

