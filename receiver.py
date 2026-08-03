from qotp import apply_qotp

# QOTP uses pauli gates which are self inverse, applying same keys removes encryption....


def received_qstate(received_circuit, x_key, z_key):
    print("Reciever")

    print("\n Encrypted quantum state is recieved")

    decrypted_circuit = apply_qotp(received_circuit, x_key, z_key)

    print("\n QOTP decryption successfull")
    print(decrypted_circuit)

    return decrypted_circuit
