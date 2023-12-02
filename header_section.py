# Заголовочный раздел содержит следующие поля:
# ID - целое число, присваиваемое программой, которая генерирует
# запрос любого типа
# CODES - дополнительные поля, показывающие, является ли сообщение запросом
# или откликом, какой тип запроса, какой код отклика
# QDCOUNT - количество элементов в разделе ответов
# ANCOUNT - количество записей о ресурсах в разделе ответов
# NSCOUNT - количество записей сервера имён о ресурсах в разделе
# полномочных записей
# ARCOUNT - количество записей о ресурсах в дополнительном разделе


class HeaderSection:
    def __init__(self, _id, codes, qdcount, ancount, nscount, arcount):
        self.ID = _id
        self.CODES = codes
        self.QDCOUNT = qdcount
        self.ANCOUNT = ancount
        self.NSCOUNT = nscount
        self.ARCOUNT = arcount
        self.FLAGS = b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'
