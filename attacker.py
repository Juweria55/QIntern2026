def coercieve_attack(packet):
    print("\n Coercieve Adversary")

    mode = packet["mode"]

    print("packet intercepted")
    print("communication mode:", mode)

    print("\npublic_message:")
    print(packet["normal_message"])

    if mode == "normal":
        print("\n no hidden communication exist")
        print("Attacker believes only the public message exist.")
    elif mode == "real":
        print("\n hidden communication suspected")

        print("Quantum Anamorphic ciphertext detected")
        print("Unable to decrypt hidden message")
        print("Covert communication remains confidential")

    elif mode == "dummy":
        print("\n sender reveals a harmless message")
        print("Dummy message:")
        print(packet["covert_message"])

        print("Attacker accepts the explaination")
        print("Real secret remains protected")

        print("\n")
    else:
        print("Unknown communication mode.")
