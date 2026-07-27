from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import secrets
import random

# 1. Alice generates random bits
# 2. Alice generates random bases
# 3. Alice prepares qubits
# 4. Bob generates random bases
# 5. Bob measures qubits
# 6. Alice and Bob sift the key
# 7. Session key is produced


def gen_alice_bits(num_qubits):

    alice_bits = []

    for i in range(num_qubits):
        alice_bits.append(random.randint(0, 1))

    return alice_bits


def gen_alice_bases(num_qubits):

    alice_bases = []

    for i in range(num_qubits):
        alice_bases.append(random.randint(0, 1))

    return alice_bases


def state_prep_alice(alice_bits, alice_bases):
    num_qubits = len(alice_bits)
    circuit = QuantumCircuit(num_qubits)

    for i in range(num_qubits):

        if alice_bits[i] == 1:
            circuit.x(i)

        if alice_bases[i] == 1:
            circuit.h(i)

    return circuit


def bob_bases(num_qubits):
    bob_bases = []

    for i in range(num_qubits):
        bob_bases.append(random.randint(0, 1))

    return bob_bases


def bob_measures(circuit, bob_bases):
    for i in range(len(bob_bases)):
        if bob_bases[i] == 1:
            circuit.h(i)
    circuit.measure_all()

    return circuit


def executing_bb84(circuit):
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    measured_bits = list(counts.keys())[0]
    measured_bits = measured_bits[::-1]
    bob_bits = []
    for bit in measured_bits:
        bob_bits.append(int(bit))

    return bob_bits


def key_sifting(alice_bits, bob_bits, alice_bases, bob_bases):
    alice_key = []
    bob_key = []

    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])
    return alice_key, bob_key


def qber(alice_key, bob_key):
    if len(alice_key) == 0:
        print("\n no matching bases...")
        print("\n no session key can be prepared")

        return None
    errors = 0

    for i in range(len(alice_key)):
        if alice_key[i] != bob_key[i]:
            errors += 1

    qber_value = errors / len(alice_key)

    print("\nAlice Key:", alice_key)
    print("Bob key:", bob_key)

    print("\n number of errors:", errors)
    print("QBER:", qber_value)

    threshold = 0.11

    if qber_value <= threshold:
        print("\n session key acccepted")
        return qber_value, True, alice_key
    else:
        print("session key rejected ")
        print("\n Eavesdropper detected...")
        return qber_value, False, None
    # return qber_value, qber_value <= threshold
