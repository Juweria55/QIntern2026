import secrets
from datetime import datetime
from packet_format import create_packet
from gateway_server import receive_packet

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
print("\n sending packets to Gtaeway... \n")


receive_packet(packet)
