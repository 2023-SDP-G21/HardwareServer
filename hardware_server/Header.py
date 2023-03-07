import struct
from dataclasses import dataclass


@dataclass
class Header:
    HEADER_LEN = 4

    heartbeat_ack: bool
    heartbeat: bool
    data_type: int
    data_len: int

    @staticmethod
    def from_bytes(header_bytes):
        heartbeat_ack, heartbeat, data_type, data_len = struct.unpack("!??BB", header_bytes)
        return Header(heartbeat_ack, heartbeat, data_type, data_len)

    def __repr__(self):
        return f"{self.heartbeat_ack} {self.heartbeat} {self.data_type} {self.data_len}"
