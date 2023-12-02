import struct


class Message:
    def __init__(self, header, question, answer, authority, additional):
        self.header = header
        self.question = question
        self.answer = answer
        self.authority = authority
        self.additional = additional

    def pack_header_and_question_sections(self, flags):
        result = bytearray()
        result += struct.pack('!H', self.header.ID) + flags
        parts = [part.encode() for part in self.question[0].QNAME.split('.')]
        encoded_parts = [struct.pack('!B', len(part)) + part for part in parts]
        question = b''.join(encoded_parts)
        question += struct.pack('!B2H', 0, 1, 1)
        result += question
        return result

    def req_to_bytearray(self):
        return self.pack_header_and_question_sections(self.header.FLAGS)
