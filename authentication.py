from Crypto.Hash import KMAC128


def gen_auth_tag(packet, shared_key):
    message = (  # combine packet into one message.....
        packet["normal_message"] +
        packet["covert_message"] +
        packet["timestamp"] +
        packet["nonce"]
    )

    message = message.encode()  # converting string into bytes
    kmac = KMAC128.new(  # generate KMAC
        key=shared_key,
        data=message,
        mac_len=32
    )
    return kmac.hexdigest()
