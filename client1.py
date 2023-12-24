import socket
import threading
import Crypto_funcs


def listener(conn, lock):
    global privkey
    while True:
        try:
            data = (conn.recv(1024))
            # print_pexpect('there is no data')
        except OSError:
            break
        if data:
            aes_key_enc, message_enc = data.split(b'@border@')
            aes_key = Crypto_funcs.rsa_decryption(privkey, aes_key_enc)
            message = Crypto_funcs.aes_decryption(message_enc, aes_key)
            with lock:
                print(message)


def encrypt(message, partner_pubkey):
    aes_key = Crypto_funcs.aes_key_generate()
    message_ciphertext = Crypto_funcs.aes_encryption(message, aes_key)
    aes_key_ciphertext = Crypto_funcs.rsa_encryption(partner_pubkey, aes_key)
    return aes_key_ciphertext + b'@border@' + message_ciphertext


PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9090))
sock.send(b'get_pubkey_2')
partner_pubkey = (sock.recv(1024))
sock.close()
file = open('client1/privkey.pem', mode='rb')
privkey = file.read()
file.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', PORT))
sock.listen()
conn, addr = sock.accept()
print(f'conntected with {addr}')
lock = threading.Lock()  # create a thread lock to allow for printing
listen_thread = threading.Thread(target=listener, args=(conn, lock),
                                 daemon=True)  # create the thread that listens for messages
listen_thread.start()
while True:
    mes = input()
    if mes != 'exit':
        conn.send(encrypt(mes.encode('utf-8'), partner_pubkey))
        mes = ''
    else:
        quit(0)
