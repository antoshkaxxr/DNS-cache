from itertools import islice
from header_section import HeaderSection
from question_section import QuestionSection
from resource_record import ResourceRecord
from message import Message


class BytesSequenceReader:
    def __init__(self, bytes_data: bytearray):
        self.bytes_data = bytes_data
        self.pointer = 0
        self.header_counts = 4

    def read_certain_size(self, size):
        subsequence = bytearray(islice(self.bytes_data, self.pointer,
                                       self.pointer + size))
        self.pointer += size
        return subsequence

    @staticmethod
    def convert_to_int(byte_number):
        return int.from_bytes(byte_number, byteorder='big')

    def read_name(self):
        name_parts = []
        while True:
            part_length = self.bytes_data[self.pointer]
            self.pointer += 1

            if part_length == 0:
                break

            if (part_length & 0xC0) == 0xC0:
                pointer_offset = ((part_length & 0x3F) << 8) + self.bytes_data[
                    self.pointer]
                self.pointer += 1
                original_pointer = self.pointer

                self.pointer = pointer_offset
                name_parts.extend(self.read_name())

                self.pointer = original_pointer
                break

            part = self.read_certain_size(part_length)
            name_parts.append(part.decode())

        return '.'.join(name_parts)

    def read_counts(self):
        counts = []
        for _ in range(self.header_counts):
            counts.append(self.convert_to_int(self.read_certain_size(2)))
        return counts

    def read_header_section(self):
        _id = self.convert_to_int(self.read_certain_size(2))
        codes = self.read_certain_size(2)
        counts = self.read_counts()
        return HeaderSection(_id, codes, *counts)

    def read_question_section(self):
        qname = self.read_name()
        qtype = self.read_certain_size(2)
        qclass = self.read_certain_size(2)
        return QuestionSection(qname, qtype, qclass)

    def read_resource_record(self):
        name = self.read_name()
        _type = self.convert_to_int(self.read_certain_size(2))
        _class = self.convert_to_int(self.read_certain_size(2))
        ttl = self.convert_to_int(self.read_certain_size(4))
        rdlength = self.convert_to_int(self.read_certain_size(2))
        rdata = self.read_certain_size(rdlength)
        return ResourceRecord(name, _type, _class, ttl, rdlength, rdata)

    def read_message(self):
        header = self.read_header_section()
        question = [self.read_question_section() for _ in range(header.QDCOUNT)]
        answer = [self.read_resource_record() for _ in range(header.ANCOUNT)]
        authority = [self.read_resource_record() for _ in range(header.NSCOUNT)]
        additional = [self.read_resource_record() for _ in range(header.ARCOUNT)]
        return Message(header, question, answer, authority, additional)
