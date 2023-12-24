import socket

sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen()
checking_flag = 0  # 0-нет проверки 1-проверка идет
blocks_to_write_list = []
while True:
    conn, addr = sock.accept()
    # conn.setblocking(False)
    print('connected:', addr)

    try:
        data = (conn.recv(1024))
        # print_pexpect('there is no data')
    except OSError:
        break
    if data:
        if data == b'get_pubkey_1':
            file = open('server/pubkey1.pem', mode='rb')
            pubkey = file.read()
            file.close()
            conn.send(pubkey)
        elif data == b'get_pubkey_2':
            file = open('server/pubkey2.pem', mode='rb')
            pubkey = file.read()
            file.close()
            conn.send(pubkey)
        conn.close()
        print(f'connection {addr} closed')
