# its gonna recieve packet, authenticate it and extract the covert message....
from quantum_encoder import quantum_encode
from shared_key import get_shared_key
from authentication import gen_auth_tag
from message_encoder import extract_binary
from bb84 import (
    gen_alice_bits,
    gen_alice_bases,
    state_prep_alice,
    bob_bases,
    bob_measures,
    executing_bb84,
    key_sifting,
    qber
)

used_nonces = set()  # check if the nonce already exist or not....


def receive_packet(packet):
    print("Gateway")
    print(" waiting to recieve the packet......")
    print()
    print("packet reccieved successfully having data:")

    for key, value in packet.items():
        print(f"{key}: {value}")

    print("\n waiting for verification........")

    if verify_packet(packet):
        if replay_attack_detection(packet):
            covert_message = covert_message_extraction(packet)

            binary_message = extract_binary(covert_message)
            print("Binary Message:", binary_message)
            quantum_circuit = quantum_encode(binary_message)
            print("Quantum state prepration is successfull.. ")
            print(quantum_circuit)
            print("\n bb84 key generation begins....")
            num_qubits = 16
            alice_bits = gen_alice_bits(num_qubits)
            alice_bases = gen_alice_bases(num_qubits)

            print("\n alice bits:", alice_bits)
            print("\n alice bases:", alice_bases)

            bb84_circuit = state_prep_alice(alice_bits, alice_bases)
            print("bb84 quantum circuit:", bb84_circuit)
            bob_basis = bob_bases(num_qubits)
            print("Bob bases:", bob_basis)

            # bob measures the qubit
            bb84_circuit = bob_measures(bb84_circuit, bob_basis)

            print("\n BB84 circuit after bob's measurement:", bb84_circuit)

            # execute the circuit
            bob_bits = executing_bb84(bb84_circuit)
            print("\n Bob bits:", bob_bits)

            # alice and bob perform key sifting''''
            alice_key, bob_key = key_sifting(
                alice_bits,
                bob_bits,
                alice_bases,
                bob_basis
            )

            print("\nAlice key:", alice_key)
            print("\nBob key:", bob_key)

            # calculate qber and gen session key
            qber_value, accepted, session_key = qber(alice_key, bob_key)
            print("\nQBER:", qber)
            print("\nAccepted:", accepted)
            if accepted:
                print("\n session key:", session_key)
            else:
                print("session key not generated.")

            print("\n Gateway acceted the packet")
        else:
            print("\nGateway rejected the packet")


def verify_packet(packet):
    print("\n verifying packet... \n")

    required_fields = ["normal_message",
                       "covert_message",
                       "timestamp",
                       "nonce",
                       "authentication_tag"
                       ]

    for field in required_fields:
        if field not in packet:
            print(f"{field} is missing")

            return False

    print("packet verification successful")
    received_tag = packet["authentication_tag"]

    # get the shared key
    shared_key = get_shared_key()

    # gen a new auth tag
    gen_tag = gen_auth_tag(packet, shared_key)

    print("\nReceived Authentication Tag:")

    print(received_tag)

    print("\nGenerated Authenticationtag:")
    print(gen_tag)

    if received_tag == gen_tag:
        print("\nAuthentication successful")
        return True
    else:
        print("\nAuthentication failed")
        return False


def replay_attack_detection(packet):
    nonce = packet["nonce"]
    if nonce in used_nonces:
        print("\n Replay attack detected..")
        return False
    used_nonces.add(nonce)

    print("\nnonce accepted....")
    print("Packet is fresh.")

    return True


def covert_message_extraction(packet):
    covert_message = packet["covert_message"]
    print("Extraction of covert message is being done....")
    print("Covert Message:", covert_message)
    return covert_message


# print(ord("A"))
# print(ord("B"))
# print(ord("w"))
# print(format(65, "08b"))
# print(format(66, "08b"))
# print(format(119, "08b"))
