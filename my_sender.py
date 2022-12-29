#  client that sends the alarm

import usocket
import utime


BUFFER_SIZE = 1024


def send_alarm (host, port):
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    print(f'[+] Connecting to {host}:{port}')

    s.connect((host, port))

    print(f'[+] Connected to server')

    send_data = b'you have got a gate IR alarm'

    s.send(send_data)

    s.close()
