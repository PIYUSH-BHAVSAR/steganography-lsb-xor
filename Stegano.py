import cv2
import numpy as np

# Encrypt Message Using XOR Key
def encrypt_message(message, key):
    """Encrypt message using XOR cipher with repeating key"""
    message_bin = ''.join(format(ord(char), '08b') for char in message)
    key_bin = ''.join(format(ord(k), '08b') for k in key)
    key_len = len(key_bin)

    encrypted_bin = ''.join(
        str(int(message_bin[i]) ^ int(key_bin[i % key_len])) 
        for i in range(len(message_bin))
    )
    return encrypted_bin

# Embed Encrypted Message in Image Binary (LSB)
def embed_message(binary_string, encrypted_message):
    """Embed encrypted message into image binary using LSB technique"""
    binary_list = list(binary_string)

    # Store message length as a 32-bit binary header
    message_length = format(len(encrypted_message), '032b')
    full_message = message_length + encrypted_message

    msg_index = 0
    for i in range(0, len(binary_list), 8):
        if msg_index < len(full_message):
            binary_list[i + 7] = full_message[msg_index]  # Replace LSB
            msg_index += 1
        else:
            break

    return ''.join(binary_list)

# Extract Encrypted Message
def extract_encrypted_message(binary_string):
    """Extract encrypted message from stego image binary"""
    # Extract message length from first 32 LSBs
    message_length_bin = ''.join([binary_string[i + 7] for i in range(0, 32 * 8, 8)])
    message_length = int(message_length_bin, 2)

    # Extract the actual message
    extracted_bits = [
        binary_string[i + 7] 
        for i in range(32 * 8, (32 + message_length) * 8, 8)
    ]
    return ''.join(extracted_bits)

# Decrypt Message
def decrypt_message(encrypted_bin, key):
    """Decrypt message using XOR cipher"""
    key_bin = ''.join(format(ord(k), '08b') for k in key)
    key_len = len(key_bin)

    decrypted_bin = ''.join(
        str(int(encrypted_bin[i]) ^ int(key_bin[i % key_len])) 
        for i in range(len(encrypted_bin))
    )
    message = ''.join(
        chr(int(decrypted_bin[i:i+8], 2)) 
        for i in range(0, len(decrypted_bin), 8)
    )
    return message.strip()