# Command structure:
# Byte 0: Command ID
# Byte 1: Command Data Length (MSB)
# Byte 2: Command Data Length (LSB)
# Byte 3: Command data (0)
# Byte 4: Command data (1)
# ...
# Byte n: Command data (n-3)
# Byte n+1: Checksum (MSB)
# Byte n+2: Checksum (LSB)
# Byte n+3: End of command (0x0D)

# For checksum calculation we use CRC32 algorithm, which is implemented in the ESP32 microcontroller
# Checksum is calculated from the first byte of the command to the last byte of the command data

from zlib import crc32

class Command:
    # Default constructor
    def __init__(self, cmd_id, data):
        self.cmd_id = cmd_id
        self.data = data
        self.length = len(data)

    # Constructor for creating a command from a byte array
    @classmethod
    def from_bytes(cls, bytes):
        cmd_id = bytes[0]
        length = (bytes[1] << 8) + bytes[2]
        data = bytes[3:3+length]
        # check if the provided checksum is correct
        checksum = (bytes[3+length] << 8) + bytes[3+length+1]
        if checksum != cls(cmd_id, data).get_checksum():
            raise ValueError("Invalid checksum")
        return cls(cmd_id, data)

    # Constructor for creating a command from a stream of bytes
    @classmethod
    def from_stream(cls, stream):
        cmd_id = stream.read(1)[0]
        length = (stream.read(1)[0] << 8) + stream.read(1)[0]
        data = stream.read(length)
        # check if the provided checksum is correct
        checksum = (stream.read(1)[0] << 8) + stream.read(1)[0]
        if checksum != cls(cmd_id, data).get_checksum():
            raise ValueError("Invalid checksum")
        return cls(cmd_id, data)

    def __str__(self):
        return "Command ID: " + str(self.cmd_id) + "\nCommand length: " + str(self.length) + "\nCommand data: " + str(self.data)

    def get_bytes(self):
        bytes = bytearray()
        bytes.append(self.cmd_id)
        bytes.append((self.length >> 8) & 0xFF)
        bytes.append(self.length & 0xFF)
        for i in range(self.length):
            bytes.append(self.data[i])
        return bytes

    def get_checksum(self):
        bytes = bytearray()
        bytes.append(self.cmd_id)
        bytes.append((self.length >> 8) & 0xFF)
        bytes.append(self.length & 0xFF)
        checksum = crc32(bytes)
        
        return checksum

    def get_checksum_bytes(self):
        return bytearray([(self.get_checksum() >> 8) & 0xFF, self.get_checksum() & 0xFF])

    def get_end_bytes(self):
        return bytearray([0x0D])

    def get_full_bytes(self):
        return self.get_bytes() + self.get_checksum_bytes() + self.get_end_bytes()