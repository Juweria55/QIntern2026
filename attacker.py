def coercieve_attack(packet):
    print("\n Coercieve Adversary")

    mode = packet["mode"]

    print("packet intercepted")

    print("\npublic_message:")
    print(packet["normal_message"])

    if mode == "normal":
        print("no hidden communication exist")
    elif mode == "real":
        print("\n hidden communication suspected")

        print("Quantum Anamorphic ciphertext can be decrypted")
        print("the hidden message remains secret")

    elif mode == "dummy":
        print("\n sender reveals a harmless message")

        print("Attacker accepts the explaination")

        print("\n")
