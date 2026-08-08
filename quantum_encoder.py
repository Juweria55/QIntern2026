from qiskit import QuantumCircuit


def quantum_encode(binary_message):
    num_qubits = len(binary_message)

    circuit = QuantumCircuit(num_qubits)

    for i, bit in enumerate(binary_message):
        if bit == "1":
            circuit.x(i)

    return circuit
