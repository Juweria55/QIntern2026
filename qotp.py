

def gene_qotp_keys(session_key, num_qubits):
    x_key = []
    z_key = []

    for i in range(num_qubits):
        x_key.append(session_key[i])
        z_key.append(session_key[i + num_qubits])
    return x_key, z_key


def apply_qotp(circuit, x_key, z_key):
    for i in range(len(x_key)):
        if x_key[i] == 1:
            circuit.x(i)

        if z_key[i] == 1:
            circuit.z(i)
    return circuit
