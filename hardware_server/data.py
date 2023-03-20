import struct
from dataclasses import dataclass


@dataclass
class Data:
    angle: int
    power: int

    @staticmethod
    def from_bytes(data_bytes):
        try:
            angle, power = struct.unpack("!ii", data_bytes)
            if angle in range(-180, 181) and power in range(0, 101):
                return Data(angle, power)
            else:
                raise struct.error
        except struct.error:
            print("Could not unpack")

    def __repr__(self):
        return f"Angle: {self.angle}, Power: {self.power}"
