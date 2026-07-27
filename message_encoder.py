# this file is gonna convert message into binary, later those values will be encoded into the quantum state...

def extract_binary(message):
    # initially no binary, se we are starting with the empty strijng...
    binary_message = ""

    for char in message:
        ascii_value = ord(char)

        # converts to binary, always use 8 bits and pad with leading 0 if needed
        binary_char = format(ascii_value, "08b")

        binary_message += binary_char

    return binary_message
