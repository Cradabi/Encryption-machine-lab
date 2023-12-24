import rsa
import pyaes
from string import ascii_letters, digits
from secrets import choice


def aes_key_generate():
    # A random 256 bit (32 byte) key
    al = digits + ascii_letters
    key = ''
    key_len = 32
    for i in range(key_len):
        key += choice(al)

    # key must be bytes
    return key.encode('utf-8')


def aes_encryption(plaintext, key):
    aes = pyaes.AESModeOfOperationCTR(key)
    return aes.encrypt(plaintext)


def aes_decryption(ciphertext, key):
    # CRT mode decryption requires a new instance be created
    aes = pyaes.AESModeOfOperationCTR(key)

    # decrypted data is always binary, need to decode to plaintext
    return aes.decrypt(ciphertext).decode('utf-8')


def rsa_keys_generate():
    (pubkey, privkey) = rsa.newkeys(1024)  # 1024 bits key length

    pubkey_pem = pubkey.save_pkcs1()  # (format='PEM')
    privkey_pem = privkey.save_pkcs1()
    return privkey_pem, pubkey_pem


def rsa_encryption(pubkey_pem, plaintext):
    pubkey = rsa.PublicKey.load_pkcs1(pubkey_pem, 'PEM')  # (keyfile:bytes, format='PEM')
    return rsa.encrypt(plaintext, pubkey)


def rsa_decryption(privkey_pem, ciphertext):
    privkey = rsa.PrivateKey.load_pkcs1(privkey_pem, 'PEM')  # (keyfile:bytes, format='PEM')
    return rsa.decrypt(ciphertext, privkey)


def test_functions(test_text):  # if something doesnt work u can activate this function and find what u need
    test_key = aes_key_generate()
    print(test_key)
    privkey_pem, pubkey_pem = rsa_keys_generate()

    test_aes_text = aes_encryption(test_text, test_key)
    test_key = rsa_encryption(pubkey_pem, test_key)

    test_key = rsa_decryption(privkey_pem, test_key)

    print(test_key)
    print(aes_decryption(test_aes_text, test_key))

# test_functions('test 123 ! - () * & ^ TEST')
