import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    client_socket.connect(server_address)

    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        client_socket.sendall(msg.encode('utf-8'))

        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        BUFFER_SZIE = 16
        while True:
            chunk = client_socket.recv(BUFFER_SZIE)
            received_message += chunk.decode()
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            if len(chunk) < BUFFER_SZIE:
                print('Done receiving')
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        print('closing socket', file=log_buffer)
        client_socket.close()

        # you received from the server as the return value of this function.
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
