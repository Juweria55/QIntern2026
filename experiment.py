import secrets
from datetime import datetime

from packet_format import create_packet
from gateway_server import receive_packet
from shared_key import get_shared_key
from authentication import gen_auth_tag
from anamorphic import create_public_message, create_hidden_message
from attacker import coercieve_attack


message_sizes = [2, 5, 10, 20, 50, 100]

# Communication modes
modes = ["normal", "real", "dummy"]

# no of repitition for each experiments
number_of_runs = 1


# Test each communication mode
for mode in modes:

    print("\n Testing mode:", mode)

    # Test each message size
    for size in message_sizes:
        print("\n Message size:", size)
        print("Mode:", mode)

        # Create public message
        public_text = "N" * size

        # Create hidden message according to mode
        if mode == "normal":
            hidden_text = "S" * size

        elif mode == "real":
            hidden_text = "D" * size

        elif mode == "dummy":
            hidden_text = "Meet me at 5 PM."

        # Create messages
        normal_message = create_public_message(public_text)
        covert_message = create_hidden_message(hidden_text)

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate nonce
        nonce = secrets.token_hex(8)

        # Initially empty authentication tag
        authentication_tag = ""

        # Create packet
        packet = create_packet(
            normal_message,
            covert_message,
            timestamp,
            nonce,
            authentication_tag,
            mode
        )

        # Generate authentication tag
        shared_key = get_shared_key()

        authentication_tag = gen_auth_tag(
            packet,
            shared_key
        )

        packet["authentication_tag"] = authentication_tag

        print("\nPacket created successfully")

        # Simulate coercive attacker
        coercieve_attack(packet)

        # Run the complete protocol
        receive_packet(packet)

        print("\nExperiment completed")
