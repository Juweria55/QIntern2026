# its gonna recieve packet, authenticate it and extract the covert message....
from quantum_encoder import quantum_encode
from shared_key import get_shared_key
from authentication import gen_auth_tag
from message_encoder import extract_binary
from qotp import gene_qotp_keys, apply_qotp
from quantum_channel import trans_qstate
from receiver import received_qstate
from message_decoder import measure_qstate, bin_to_text
import time
from performance import save_result

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

from anamorphic import (
    create_public_message,
    create_hidden_message,
    create_anamorphic_ciphertext
)

used_nonces = set()  # check if the nonce already exist or not....


def receive_packet(packet):
    total_start = time.perf_counter()
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

            bb84_start = time.perf_counter()
            print("\n bb84 key generation begins....")

            session_key = []
            alice_key = []
            bob_key = []
            accepted = False
            qber_value = None

            qotp_enc_time = 0
            qotp_dec_time = 0

            while len(session_key) < 2 * len(binary_message):
                num_qubits = 128
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

                result = qber(alice_key, bob_key)
                if result is not None:
                    qber_value, accepted, key = result

                if accepted:
                    session_key.extend(key)
                session_key = session_key[:2 * len(binary_message)]
                # accepted = True

            bb84_end = time.perf_counter()
            bb84_time = bb84_end - bb84_start

            # calculate qber and gen session key
            # qber_value, accepted, session_key = qber(alice_key, bob_key)

            print("\nAlice key:", alice_key)
            print("\nBob key:", bob_key)

            print("Binary length:", len(binary_message))
            # print("Session key:", session_key)
            # print("Session key length:", len(session_key))

            if len(session_key) > 0:

                print("session key:", session_key)
                print("session key length:", len(session_key))
            else:
                print("session key is not generated.")

            if accepted:
                x_key, z_key = gene_qotp_keys(session_key, len(binary_message))

                print("\n X key:", x_key)
                print("\n Z key:", z_key)

                qotp_enc_start = time.perf_counter()

                encrypted_circuit = apply_qotp(quantum_circuit, x_key, z_key)

                qotp_enc_end = time.perf_counter()
                qotp_enc_time = qotp_enc_end - qotp_enc_start

                print("\n Quntum circuit after QOTP:")
                print(encrypted_circuit)

                mode = packet["mode"]

                anamorphic_ciphertext = create_anamorphic_ciphertext(
                    encrypted_circuit,
                    mode)

                print(anamorphic_ciphertext)

                # passing encrypted channel to the reciever
                received_packet = trans_qstate(anamorphic_ciphertext)
                received_circuit = received_packet["ciphertext"]

                qotp_dec_start = time.perf_counter()

                decrypted_circuit = received_qstate(
                    received_circuit, x_key, z_key)

                qotp_dec_end = time.perf_counter()

                qotp_dec_time = qotp_dec_end - qotp_dec_start

                print("\n Decrypted circuit:")
                print(decrypted_circuit)

                recovered_binary = measure_qstate(decrypted_circuit)
                recovered_message = bin_to_text(recovered_binary)

                print("\n recovered message:", recovered_message)

            print("\nQBER:", qber_value)
            print("\nAccepted:", accepted)
            if accepted:
                print("\n session key:", session_key)
            else:
                print("session key not generated.")

            print("\n Gateway accepted the packet")
            # stopping total timeer
            total_end = time.perf_counter()
            total_time = total_end - total_start

            save_result(

                mode=mode,
                message_length=len(binary_message),
                num_qubits=num_qubits,
                session_key_length=len(session_key),
                qber=qber_value,
                bb84_time=bb84_time,
                qotp_enc_time=qotp_enc_time,
                qotp_dec_time=qotp_dec_time,
                total_time=total_time
            )

            print("\n Performance......")
            print("BB84 time:", bb84_time)
            print("QOTP Encryption time:", qotp_enc_time)
            print("QOTP Decryption time:", qotp_dec_time)
            print("Total Protoccol time:", total_time)
            print("------------------------------------")

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
