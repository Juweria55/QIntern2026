def receive_packet(packet):
    print("Gateway")
    print(" waiting to recieve the data......")
    print()
    print("packet reccieved successfully having data:")

    for key, value in packet.items():
        print(f"{key}: {value}")

    print("\n waiting for verification........")
    verify_packet(packet)


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

    return True
