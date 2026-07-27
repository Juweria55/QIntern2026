import secrets
from datetime import datetime
from packet_format import create_packet
from gateway_server import receive_packet
from shared_key import get_shared_key
from authentication import gen_auth_tag

# generate normal messagee.....
normal_message = "AUTH REQUEST..."

# create the covert text
covert_message = "we are being watched"  # or staye alert

# now generate the time stamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# let's generatr NONCE
nonce = secrets.token_hex(8)

# Authentication tagg
authentication_tag = ""

# let's create packet using packet_format.py........
packet = create_packet(
    normal_message,
    covert_message,
    timestamp,
    nonce,
    authentication_tag
)

shared_key = get_shared_key()  # get the shared keyyy

authentication_tag = gen_auth_tag(packet, shared_key)

packet["authentication_tag"] = authentication_tag

# now let's create a packet....store all the above in a dictionary to create a packet....
"""packet = {
    "normal_message": normal_message,
    "covert_message": covert_message,
    "timestamp": timestamp,  # type: ignore
    "nonce": nonce,
    "authentication_tag": authentication_tag
}

# let's see how our packet looks like....."""
print("\n---LOW RESOURCE NODE BEGINS---- \n")
print("\n Packet generated \n")

for key, value in packet.items():
    print(f"{key}: {value}")


# print(".....")
print("\n sending packets to Gtaeway... \n")
receive_packet(packet)


# to show the replay attack we can send the same packet....it will detedct the replay attack....
# because the same nonce is being sent twice even the second way we can do is to use the fixed nonce twice...nonce="123456789abcdef0"
"""print("\nFirst Transmission\n")
receive_packet(packet)

print("\nSecond Transmission (Replay Attack)\n")
receive_packet(packet)"""
