from itertools import islice


class BytesSequenceReader:
    def __init__(self, bytes_data):
        self.bytes_data = bytes_data
        self.pointer = 0

    def read_certain_size(self, size):
        subsequence = bytearray(islice(self.bytes_data, self.pointer,
                                       self.pointer + size))
        self.pointer += size
        return subsequence

    def read_int_number(self, size):
        byte_number = self.read_certain_size(size)
        return int.from_bytes(byte_number, byteorder='big')

