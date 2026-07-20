def create_packet(normal_message,
                  covert_message,
                  timestamp,
                  nonce,
                  authentication_tag):
    packet = {
        "normal_message": normal_message,
        "covert_message": covert_message,
        "timestamp": timestamp,
        "nonce": nonce,
        "authentication_tag": authentication_tag
    }
    return packet
