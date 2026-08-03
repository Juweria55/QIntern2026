from qiskit import transpile
from qiskit_aer import AerSimulator


def measure_qstate(decrypted_circuit):
    print("\n Measuring decryptede quantum state.....")

    circuit = decrypted_circuit.copy()  # copying the python obj
    circuit.measure_all()
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    measured_binary = list(counts.keys())[0]
    measured_binary = measured_binary[::-1]

    print("\n Recovered binary:", measured_binary)

    return measured_binary


def bin_to_text(binary_message):
    recovered_message = ""

    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]

        character = chr(int(byte, 2))

        recovered_message += character

    # print("\n Recovered Messsage:", recovered_message)

    return recovered_message
