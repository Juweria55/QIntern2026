from Crypto.Hash import KMAC128


def gen_auth_tag(message, shared_key):
    message = message.encode
    kmac = KMAC128.new(
        key=shared_key,
        data=message,
        mac_len=32
    )
    return kmac.hexdigest()
