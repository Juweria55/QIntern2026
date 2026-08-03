def create_public_message(message):
    return message


def create_hidden_message(message):
    return message


def create_anamorphic_ciphertext(encrypted_circuit, mode):
    print("\n constructing anamorphic ciphertext.....")

    anamorphic_ciphertext = {
        "ciphertext": encrypted_circuit,
        "mode": mode,
        "type": "Quantum Anamorphic Ciphertext"
    }

    return anamorphic_ciphertext
