import struct

def as_bytes(heartbeat_ack, heartbeat, data_type, data):
    data_encoded = data.encode("utf-8")
    data_len = len(data_encoded)
    return struct.pack("!??BB", heartbeat_ack, heartbeat, data_type, data_len) + data_encoded
